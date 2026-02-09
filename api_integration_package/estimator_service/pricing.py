"""
Pricing engine for cost estimation.
Applies unit prices to measured quantities from Takeoff data.
"""
import logging
from typing import Dict

logger = logging.getLogger(__name__)


# ========================================
# PRICING RULES (Unit Prices)
# ========================================
PRICING_RULES = {
    "window": {
        "unit_price": 200.0,
        "unit": "EA",
        "description": "Window installation (per unit)"
    },
    "door": {
        "unit_price": 300.0,
        "unit": "EA",
        "description": "Door installation (per unit)"
    },
    "wall": {
        "unit_price": 50.0,
        "unit": "SQ.M",
        "description": "Wall construction (per square meter)"
    }
}


def calculate_estimate(page_state: Dict) -> float:
    """
    Calculate cost estimate based on measured quantities and pricing rules.

    **Pricing Logic:**
    - Identifies element type from condition name (window/door/wall)
    - Extracts quantity values from takeoff items
    - Applies unit price based on element type
    - Sums total cost across all items

    **Unit Prices:**
    - Window (Count): $200 per unit
    - Door (Count): $300 per unit
    - Wall (Area): $50 per square meter

    Args:
        page_state: Dictionary containing takeoffZones with conditions and items

    Returns:
        float: Total estimated cost in dollars
    """
    total_cost = 0.0
    item_count = 0

    logger.info("🔍 Starting cost calculation...")

    # Navigate the hierarchy: TakeoffZones → Conditions → TakeoffItems → QuantityValues
    takeoff_zones = page_state.get("takeoffZones", [])

    if not takeoff_zones:
        logger.warning("⚠️  No takeoff zones found in page state")
        return 0.0

    for zone in takeoff_zones:
        zone_name = zone.get("takeoffZone", {}).get("name", "Unknown Zone")
        logger.info(f"  📍 Processing zone: {zone_name}")

        conditions = zone.get("conditions", [])

        for condition_state in conditions:
            condition = condition_state.get("condition", {})
            condition_name = condition.get("name", "Unknown Condition").lower()
            condition_type = condition.get("type", "Unknown")

            # Determine pricing category based on condition name
            pricing_category = None
            if "window" in condition_name:
                pricing_category = "window"
            elif "door" in condition_name:
                pricing_category = "door"
            elif "wall" in condition_name:
                pricing_category = "wall"

            if not pricing_category:
                logger.warning(f"    ⚠️  Unknown element type: {condition_name} - skipping")
                continue

            pricing_rule = PRICING_RULES[pricing_category]
            unit_price = pricing_rule["unit_price"]

            logger.info(
                f"    🏷️  {condition.get('name', 'N/A')} "
                f"(Type: {condition_type}, Rate: ${unit_price}/{pricing_rule['unit']})"
            )

            # Process all takeoff items for this condition
            takeoff_items = condition_state.get("takeoffItems", [])

            for item in takeoff_items:
                item_name = item.get("itemName", "Unnamed Item")
                quantity_values = item.get("quantityValues", [])

                # Sum all relevant quantity values for this item
                # For Count types: use "Count" quantity
                # For Area types: use "Area" quantity
                item_total = 0.0

                for qty_value in quantity_values:
                    qty_name = qty_value.get("name", "").lower()
                    qty_unit = qty_value.get("unitOfMeasure", "")
                    qty_val = qty_value.get("value", 0.0)

                    # Match quantity type to pricing rule
                    # Windows/Doors use "Count", Walls use "Area"
                    if pricing_category in ["window", "door"] and "count" in qty_name:
                        item_cost = qty_val * unit_price
                        item_total += item_cost
                        logger.info(
                            f"      ✓ {item_name}: {qty_val} {qty_unit} × ${unit_price} = ${item_cost:.2f}"
                        )
                    elif pricing_category == "wall" and "area" in qty_name:
                        item_cost = qty_val * unit_price
                        item_total += item_cost
                        logger.info(
                            f"      ✓ {item_name}: {qty_val} {qty_unit} × ${unit_price} = ${item_cost:.2f}"
                        )

                total_cost += item_total
                item_count += 1

    logger.info(f"✅ Calculation complete: {item_count} items processed")
    return total_cost


def format_currency(amount: float) -> str:
    """
    Format amount as currency string.

    Args:
        amount: Dollar amount

    Returns:
        Formatted string like "$1,234.56"
    """
    return f"${amount:,.2f}"
