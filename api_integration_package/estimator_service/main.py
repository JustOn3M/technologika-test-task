"""
Estimator Service API - Demo Application

Simulates a cost estimation service that:
1. Receives webhook notifications from Takeoff when measurements change
2. Fetches complete current state from Takeoff
3. Calculates cost estimate based on pricing rules
4. Logs the entire flow for demonstration
"""
import logging
import os
from uuid import UUID
from typing import Dict
import httpx
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from models import ConditionsChange, PageConditionsState
from pricing import calculate_estimate, format_currency

# ========================================
# CONFIGURATION
# ========================================
# Read Takeoff URL from environment variable (for Docker) or use localhost default
TAKEOFF_SERVICE_URL = os.getenv("TAKEOFF_SERVICE_URL", "http://localhost:8000")

# ========================================
# LOGGING CONFIGURATION
# ========================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# ========================================
# FASTAPI APPLICATION
# ========================================
app = FastAPI(
    title="Estimator Service API",
    description="""
    **Estimator Service** calculates construction project costs based on measurements from Takeoff.

    This service receives webhook notifications when measurements change in Takeoff,
    fetches the complete current state, and recalculates cost estimates using pricing rules.

    ## Integration Flow
    1. **Webhook Reception**: Takeoff sends POST notification when measurements change
    2. **State Fetch**: Estimator requests complete state from Takeoff via GET
    3. **Cost Calculation**: Pricing rules applied to measured quantities
    4. **Logging**: Complete flow logged to console for demonstration

    ## Pricing Rules
    - Windows: $200 per unit
    - Doors: $300 per unit
    - Walls: $50 per square meter
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ========================================
# CORS MIDDLEWARE (Allow all origins for demo)
# ========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========================================
# BACKGROUND TASK: FETCH STATE & CALCULATE
# ========================================

async def fetch_and_estimate(document_id: UUID, page_number: int):
    """
    Background task to fetch current state from Takeoff and calculate estimate.

    This runs asynchronously after the webhook response is sent, so Takeoff
    doesn't have to wait for the entire processing to complete.

    Args:
        document_id: UUID of the document
        page_number: Page number where changes occurred
    """
    logger.info(f"📤 Fetching full state from Takeoff...")
    logger.info(f"   URL: {TAKEOFF_SERVICE_URL}/api/Conditions/GetAllConditionsState")
    logger.info(f"   Params: documentId={document_id}, pageNumber={page_number}")

    try:
        # Make async HTTP GET request to Takeoff service
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{TAKEOFF_SERVICE_URL}/api/Conditions/GetAllConditionsState",
                params={
                    "documentId": str(document_id),
                    "pageNumber": page_number
                }
            )

            if response.status_code == 200:
                # Successfully fetched state
                page_state = response.json()

                # Log state summary
                total_zones = len(page_state.get("takeoffZones", []))
                total_conditions = sum(
                    len(zone.get("conditions", []))
                    for zone in page_state.get("takeoffZones", [])
                )
                total_items = sum(
                    len(condition.get("takeoffItems", []))
                    for zone in page_state.get("takeoffZones", [])
                    for condition in zone.get("conditions", [])
                )

                logger.info(
                    f"✅ Retrieved state: {total_zones} zone(s), "
                    f"{total_conditions} condition(s), {total_items} item(s)"
                )

                # Calculate cost estimate using pricing rules
                logger.info("💰 Calculating cost estimate...")
                total_cost = calculate_estimate(page_state)

                logger.info("=" * 60)
                logger.info(f"💵 ESTIMATED COST: {format_currency(total_cost)}")
                logger.info("=" * 60)

            else:
                # Non-200 response
                logger.error(
                    f"❌ Failed to fetch state from Takeoff: "
                    f"HTTP {response.status_code}"
                )
                logger.error(f"   Response: {response.text}")

    except httpx.ConnectError:
        logger.error(
            f"❌ Cannot connect to Takeoff Service at {TAKEOFF_SERVICE_URL}"
        )
        logger.error(
            "   Make sure Takeoff service is running on port 8000"
        )
    except httpx.TimeoutException:
        logger.error("❌ Request to Takeoff service timed out")
    except Exception as e:
        logger.error(f"❌ Unexpected error during fetch and estimate: {e}")
        logger.exception(e)


# ========================================
# API ENDPOINTS
# ========================================

@app.post(
    "/api/Conditions/PostConditionsChange",
    summary="Webhook: Receive notification about measurement changes",
    description="""
    **Webhook endpoint** called by Takeoff when users create, update, or delete measurements.

    **Flow:**
    1. Receive webhook with change notification
    2. Log the changes (action types, entity types)
    3. Trigger background task to fetch full state and calculate estimate
    4. Return immediate response (Takeoff doesn't wait for calculation)

    **Background Processing:**
    - Fetches complete state from Takeoff via GET request
    - Applies pricing rules to measured quantities
    - Logs estimated cost to console

    **Actions Supported:**
    - Create: New TakeoffZone, Condition, or TakeoffItem
    - Update: Modified existing entities
    - Delete: Removed entities
    """,
    tags=["Webhooks"],
    responses={
        200: {
            "description": "Webhook received and processing started",
            "content": {
                "application/json": {
                    "example": {
                        "status": "accepted",
                        "message": "Change notification received. Processing in background."
                    }
                }
            }
        }
    }
)
async def post_conditions_change(
    conditions_change: ConditionsChange,
    background_tasks: BackgroundTasks
):
    """
    Receive webhook notification from Takeoff about measurement changes.

    This endpoint logs the changes and triggers background processing to
    fetch the complete state and recalculate the cost estimate.

    Args:
        conditions_change: Webhook payload with documentId, pageNumber, and actions
        background_tasks: FastAPI background task manager

    Returns:
        Immediate acknowledgment response
    """
    logger.info("=" * 60)
    logger.info("📥 WEBHOOK RECEIVED: PostConditionsChange")
    logger.info("=" * 60)
    logger.info(f"   Document ID: {conditions_change.documentId}")
    logger.info(f"   Page Number: {conditions_change.pageNumber}")

    # Log each action in the webhook
    actions = conditions_change.actions or []
    logger.info(f"   Actions: {len(actions)} change(s)")

    for action in actions:
        action_name = action.actionName or "Unknown"
        entity_type = action.entityType or "Unknown"
        order = action.orderNumber

        # Get entity name if available
        entity_name = "N/A"
        if action.condition and action.condition.name:
            entity_name = action.condition.name
        elif action.takeoffZone and action.takeoffZone.name:
            entity_name = action.takeoffZone.name
        elif action.takeoffItem and action.takeoffItem.itemName:
            entity_name = action.takeoffItem.itemName

        logger.info(
            f"     [{order}] {action_name} {entity_type} "
            f"({entity_name})"
        )

    # Schedule background task to fetch state and calculate estimate
    # This allows us to return immediate response to Takeoff
    background_tasks.add_task(
        fetch_and_estimate,
        conditions_change.documentId,
        conditions_change.pageNumber
    )

    logger.info("✅ Webhook accepted. Starting background processing...")

    return {
        "status": "accepted",
        "message": "Change notification received. Processing in background.",
        "documentId": str(conditions_change.documentId),
        "pageNumber": conditions_change.pageNumber,
        "actionsReceived": len(actions)
    }


@app.get(
    "/",
    summary="API Information",
    tags=["Info"]
)
async def root():
    """Root endpoint with API information."""
    return {
        "service": "Estimator Service API",
        "version": "1.0.0",
        "description": "Cost estimation service for AEC integration",
        "integration": {
            "receives_webhooks_from": "Takeoff Service (port 8000)",
            "webhook_endpoint": "/api/Conditions/PostConditionsChange"
        },
        "endpoints": {
            "swagger_ui": "/docs",
            "redoc": "/redoc"
        }
    }


@app.get(
    "/health",
    summary="Health Check",
    tags=["Info"]
)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "estimator-service",
        "takeoff_url": TAKEOFF_SERVICE_URL
    }


# ========================================
# APPLICATION STARTUP
# ========================================
if __name__ == "__main__":
    import uvicorn

    logger.info("🚀 Starting Estimator Service...")
    logger.info(f"🔗 Will connect to Takeoff Service at: {TAKEOFF_SERVICE_URL}")
    logger.info("📊 Swagger UI will be available at: http://localhost:8001/docs")
    logger.info("📖 ReDoc will be available at: http://localhost:8001/redoc")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,  # Auto-reload on code changes (development only)
        log_level="info"
    )
