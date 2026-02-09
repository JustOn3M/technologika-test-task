"""
Takeoff Service API - Demo Application

Simulates a construction measurement service that provides takeoff data
(measurements from construction drawings) to the Estimator service.

This service implements the GET endpoint that Estimator calls to retrieve
the complete current state after receiving a webhook notification.
"""
import logging
from uuid import UUID
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from models import PageConditionsState
from mock_data import get_mock_page_state

# ========================================
# LOGGING CONFIGURATION
# ========================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ========================================
# FASTAPI APPLICATION
# ========================================
app = FastAPI(
    title="Takeoff Service API",
    description="""
    **Takeoff Service** provides construction measurement data from drawings.

    This service stores measurements (windows, doors, walls, etc.) taken from
    construction drawings and provides them to the Estimator service for cost calculation.

    ## Key Features
    - Computer vision-based measurement extraction
    - Scaled drawings with DPI and scale factor (e.g., 1:100)
    - Hierarchical data: TakeoffZones → Conditions → TakeoffItems
    - Measurements include coordinates, quantities, and metadata

    ## Integration Flow
    1. User creates/modifies measurements in Takeoff UI
    2. Takeoff sends webhook to Estimator (POST /api/Conditions/PostConditionsChange)
    3. **Estimator calls this GET endpoint to retrieve full current state**
    4. Estimator recalculates cost estimate based on updated measurements
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
# API ENDPOINTS
# ========================================

@app.get(
    "/api/Conditions/GetAllConditionsState",
    response_model=PageConditionsState,
    summary="Get current state of all conditions for a document page",
    description="""
    Returns the complete measurement hierarchy for a construction drawing page.

    **What Estimator Receives:**
    - **TakeoffZones**: Scaled regions on the drawing (scale factor, DPI, boundaries)
    - **Conditions**: Types of construction elements (Window, Door, Wall) with measurement rules
    - **TakeoffItems**: Specific measurement instances with coordinates and calculated quantities
    - **QuantityValues**: Actual measured values (counts, areas, lengths)

    **Typical Response Structure:**
    ```
    PageConditionsState
    └── TakeoffZones[] (e.g., "First Floor Plan - Scale 1:100")
        └── Conditions[] (e.g., "Standard Window", "Interior Door", "Exterior Wall")
            └── TakeoffItems[] (specific instances with coordinates)
                └── QuantityValues[] (Count: 1 EA, Area: 1.8 SQ.M, etc.)
    ```

    **Called By:** Estimator service after receiving a webhook notification about changes.

    **Data Flow:**
    1. Estimator receives webhook: "Something changed in document X, page Y"
    2. Estimator calls this endpoint to get the full current state
    3. Estimator uses the complete data to recalculate cost estimate
    """,
    tags=["Conditions"],
    responses={
        200: {
            "description": "Current state retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "takeoffZones": [
                            {
                                "takeoffZone": {
                                    "id": "a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d",
                                    "name": "First Floor Plan",
                                    "scale": 100.0,
                                    "dpi": 300
                                },
                                "conditions": [
                                    {
                                        "condition": {
                                            "name": "Standard Window",
                                            "type": "Count",
                                            "shape": "Rectangle"
                                        },
                                        "takeoffItems": [
                                            {
                                                "itemName": "Window #1 - Living Room",
                                                "quantityValues": [
                                                    {"name": "Count", "value": 1.0, "unitOfMeasure": "EA"}
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }
    }
)
async def get_all_conditions_state(
    documentId: UUID = Query(
        ...,
        description="Unique identifier of the construction document/drawing"
    ),
    pageNumber: int = Query(
        ...,
        ge=1,
        description="Page number within the document (1-indexed)"
    )
) -> PageConditionsState:
    """
    Retrieve complete measurement state for a document page.

    This endpoint returns all measurement data that Estimator needs to calculate costs:
    - All takeoff zones (scaled regions) on the page
    - All conditions (types of elements) measured in each zone
    - All takeoff items (specific instances) with coordinates
    - All quantity values (calculated measurements)

    Args:
        documentId: UUID of the construction document
        pageNumber: Page number (1-indexed)

    Returns:
        PageConditionsState: Complete hierarchy of measurements
    """
    logger.info(
        f"📤 GET /api/Conditions/GetAllConditionsState - "
        f"documentId={documentId}, pageNumber={pageNumber}"
    )

    # Retrieve mock data (in production, this would query a database)
    page_state = get_mock_page_state(str(documentId), pageNumber)

    # Log summary of returned data
    total_zones = len(page_state.takeoffZones) if page_state.takeoffZones else 0
    total_conditions = sum(
        len(zone.conditions) if zone.conditions else 0
        for zone in (page_state.takeoffZones or [])
    )
    total_items = sum(
        len(condition.takeoffItems) if condition.takeoffItems else 0
        for zone in (page_state.takeoffZones or [])
        for condition in (zone.conditions or [])
    )

    logger.info(
        f"✅ Returning state: {total_zones} zone(s), "
        f"{total_conditions} condition(s), {total_items} item(s)"
    )

    return page_state


@app.get(
    "/",
    summary="API Information",
    tags=["Info"]
)
async def root():
    """Root endpoint with API information."""
    return {
        "service": "Takeoff Service API",
        "version": "1.0.0",
        "description": "Construction measurement data provider for AEC integration",
        "endpoints": {
            "swagger_ui": "/docs",
            "redoc": "/redoc",
            "get_conditions_state": "/api/Conditions/GetAllConditionsState"
        }
    }


@app.get(
    "/health",
    summary="Health Check",
    tags=["Info"]
)
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "takeoff-service"}


# ========================================
# APPLICATION STARTUP
# ========================================
if __name__ == "__main__":
    import uvicorn

    logger.info("🚀 Starting Takeoff Service...")
    logger.info("📊 Swagger UI will be available at: http://localhost:8000/docs")
    logger.info("📖 ReDoc will be available at: http://localhost:8000/redoc")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes (development only)
        log_level="info"
    )
