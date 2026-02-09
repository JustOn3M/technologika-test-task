"""
Mock data generator for Takeoff Service.
Returns hardcoded realistic construction measurement data.
"""
from uuid import UUID, uuid4
from models import (
    PageConditionsState,
    TakeoffZoneState,
    TakeoffZoneDto,
    NormalizedBoundingBoxModel,
    ConditionState,
    ConditionDto,
    TakeoffItemDto,
    QuantityDto,
    QuantityValue,
    Point,
    NameValuePair
)


def get_mock_page_state(document_id: str, page_number: int) -> PageConditionsState:
    """
    Generate realistic mock data for a construction drawing page.

    Returns a complete hierarchy:
    - 1 TakeoffZone (Floor Plan at 1:100 scale)
    - 3 Conditions (Window, Door, Wall)
    - 5 Total TakeoffItems (2 windows, 1 door, 2 walls)

    Args:
        document_id: UUID of the construction document
        page_number: Page number (1-indexed)

    Returns:
        PageConditionsState with complete measurement data
    """

    # Generate consistent UUIDs for this mock data
    zone_id = UUID("a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d")

    # Condition IDs
    window_condition_id = UUID("f1e2d3c4-b5a6-4c5d-8e9f-0a1b2c3d4e5f")
    door_condition_id = UUID("e2d3c4b5-a6f7-4c5d-8e9f-0a1b2c3d4e5f")
    wall_condition_id = UUID("d3c4b5a6-f7e8-4c5d-8e9f-0a1b2c3d4e5f")

    # TakeoffItem IDs
    window_item_1_id = UUID("b2c3d4e5-f6a7-4b5c-8d9e-0f1a2b3c4d5e")
    window_item_2_id = UUID("c3d4e5f6-a7b8-4c5d-8e9f-0a1b2c3d4e5f")
    door_item_1_id = UUID("d4e5f6a7-b8c9-4d5e-8f9a-0b1c2d3e4f5a")
    wall_item_1_id = UUID("e5f6a7b8-c9d0-4e5f-8a9b-0c1d2e3f4a5b")
    wall_item_2_id = UUID("f6a7b8c9-d0e1-4f5a-8b9c-0d1e2f3a4b5c")

    # ========================================
    # TAKEOFF ZONE: First Floor Plan (1:100 scale)
    # ========================================
    takeoff_zone = TakeoffZoneDto(
        id=zone_id,
        scale=100.0,  # 1:100 architectural scale (1 drawing unit = 100 real units)
        name="First Floor Plan",
        dpi=300,  # High-quality scanned drawing
        boundingBox=NormalizedBoundingBoxModel(
            left=0.1,
            top=0.1,
            right=0.9,
            bottom=0.9
        )
    )

    # ========================================
    # CONDITION 1: Windows
    # ========================================
    window_condition = ConditionDto(
        id=window_condition_id,
        name="Standard Window",
        type="Count",  # Discrete counting (1, 2, 3... windows)
        shape="Rectangle",
        category="Windows",
        description="Standard residential window",
        layer="WINDOWS",
        color="#3498db",  # Blue color
        lineStyle="Solid",
        fillPattern="None",
        isAttachment=False,
        quantities=[
            QuantityDto(
                name="Count",
                unitOfMeasure="EA",  # Each
                excludeAttachments=False
            ),
            QuantityDto(
                name="Area",
                unitOfMeasure="SQ.M",
                excludeAttachments=False
            )
        ],
        properties=[
            NameValuePair(name="Width", value="1200"),
            NameValuePair(name="Height", value="1500"),
            NameValuePair(name="Material", value="PVC")
        ],
        customAttributes=[
            NameValuePair(name="EnergyRating", value="A+"),
            NameValuePair(name="GlazingType", value="Double")
        ]
    )

    # Window Item 1: Living room window
    window_item_1 = TakeoffItemDto(
        id=window_item_1_id,
        conditionId=window_condition_id,
        takeoffZoneId=zone_id,
        parentTakeoffItemId=None,  # Standalone item
        itemName="Window #1 - Living Room",
        angle=0.0,  # No rotation
        points=[
            Point(x=150.5, y=200.3),  # Top-left corner
            Point(x=180.5, y=200.3),  # Top-right corner
            Point(x=180.5, y=237.8),  # Bottom-right corner
            Point(x=150.5, y=237.8)   # Bottom-left corner
        ],
        quantityValues=[
            QuantityValue(name="Count", unitOfMeasure="EA", value=1.0),
            QuantityValue(name="Area", unitOfMeasure="SQ.M", value=1.8)  # 1.2m × 1.5m
        ]
    )

    # Window Item 2: Bedroom window
    window_item_2 = TakeoffItemDto(
        id=window_item_2_id,
        conditionId=window_condition_id,
        takeoffZoneId=zone_id,
        parentTakeoffItemId=None,
        itemName="Window #2 - Bedroom",
        angle=0.0,
        points=[
            Point(x=450.0, y=180.0),
            Point(x=480.0, y=180.0),
            Point(x=480.0, y=217.5),
            Point(x=450.0, y=217.5)
        ],
        quantityValues=[
            QuantityValue(name="Count", unitOfMeasure="EA", value=1.0),
            QuantityValue(name="Area", unitOfMeasure="SQ.M", value=1.8)
        ]
    )

    # ========================================
    # CONDITION 2: Doors
    # ========================================
    door_condition = ConditionDto(
        id=door_condition_id,
        name="Interior Door",
        type="Count",
        shape="Door",
        category="Doors",
        description="Standard interior door with frame",
        layer="DOORS",
        color="#e74c3c",  # Red color
        lineStyle="Solid",
        fillPattern="None",
        isAttachment=False,
        quantities=[
            QuantityDto(
                name="Count",
                unitOfMeasure="EA",
                excludeAttachments=False
            )
        ],
        properties=[
            NameValuePair(name="Width", value="900"),
            NameValuePair(name="Height", value="2100"),
            NameValuePair(name="Material", value="Wood")
        ],
        customAttributes=[
            NameValuePair(name="FireRating", value="30min"),
            NameValuePair(name="HandleType", value="Lever")
        ]
    )

    # Door Item 1: Main entrance
    door_item_1 = TakeoffItemDto(
        id=door_item_1_id,
        conditionId=door_condition_id,
        takeoffZoneId=zone_id,
        parentTakeoffItemId=None,
        itemName="Door #1 - Main Entrance",
        angle=90.0,  # Door opens at 90 degrees
        points=[
            Point(x=300.0, y=150.0),  # Hinge side
            Point(x=327.0, y=150.0),  # Opening side
            Point(x=327.0, y=213.0),  # Bottom opening side
            Point(x=300.0, y=213.0)   # Bottom hinge side
        ],
        quantityValues=[
            QuantityValue(name="Count", unitOfMeasure="EA", value=1.0)
        ]
    )

    # ========================================
    # CONDITION 3: Walls (Area measurement)
    # ========================================
    wall_condition = ConditionDto(
        id=wall_condition_id,
        name="Exterior Wall",
        type="Area",  # Area measurement (square meters)
        shape="Polygon",
        category="Walls",
        description="Exterior wall with insulation",
        layer="WALLS",
        color="#95a5a6",  # Gray color
        lineStyle="Solid",
        fillPattern="Solid",
        isAttachment=False,
        quantities=[
            QuantityDto(
                name="Area",
                unitOfMeasure="SQ.M",
                excludeAttachments=False
            ),
            QuantityDto(
                name="Length",
                unitOfMeasure="M",
                excludeAttachments=False
            )
        ],
        properties=[
            NameValuePair(name="Thickness", value="300"),
            NameValuePair(name="Material", value="Brick"),
            NameValuePair(name="Insulation", value="Mineral Wool")
        ],
        customAttributes=[
            NameValuePair(name="ThermalResistance", value="3.5"),
            NameValuePair(name="LoadBearing", value="Yes")
        ]
    )

    # Wall Item 1: North wall
    wall_item_1 = TakeoffItemDto(
        id=wall_item_1_id,
        conditionId=wall_condition_id,
        takeoffZoneId=zone_id,
        parentTakeoffItemId=None,
        itemName="Wall #1 - North Wall",
        angle=None,
        points=[
            Point(x=100.0, y=100.0),  # Top-left corner
            Point(x=600.0, y=100.0),  # Top-right corner
            Point(x=600.0, y=130.0),  # Bottom-right (wall thickness)
            Point(x=100.0, y=130.0)   # Bottom-left
        ],
        quantityValues=[
            QuantityValue(name="Area", unitOfMeasure="SQ.M", value=15.5),  # 5m × 3.1m height
            QuantityValue(name="Length", unitOfMeasure="M", value=5.0)
        ]
    )

    # Wall Item 2: East wall
    wall_item_2 = TakeoffItemDto(
        id=wall_item_2_id,
        conditionId=wall_condition_id,
        takeoffZoneId=zone_id,
        parentTakeoffItemId=None,
        itemName="Wall #2 - East Wall",
        angle=None,
        points=[
            Point(x=600.0, y=100.0),
            Point(x=630.0, y=100.0),
            Point(x=630.0, y=500.0),
            Point(x=600.0, y=500.0)
        ],
        quantityValues=[
            QuantityValue(name="Area", unitOfMeasure="SQ.M", value=12.4),  # 4m × 3.1m height
            QuantityValue(name="Length", unitOfMeasure="M", value=4.0)
        ]
    )

    # ========================================
    # ASSEMBLE COMPLETE STATE HIERARCHY
    # ========================================

    # Condition State 1: Windows with items
    window_condition_state = ConditionState(
        condition=window_condition,
        takeoffItems=[window_item_1, window_item_2]
    )

    # Condition State 2: Doors with items
    door_condition_state = ConditionState(
        condition=door_condition,
        takeoffItems=[door_item_1]
    )

    # Condition State 3: Walls with items
    wall_condition_state = ConditionState(
        condition=wall_condition,
        takeoffItems=[wall_item_1, wall_item_2]
    )

    # Takeoff Zone State with all conditions
    zone_state = TakeoffZoneState(
        takeoffZone=takeoff_zone,
        conditions=[
            window_condition_state,
            door_condition_state,
            wall_condition_state
        ]
    )

    # Page State (root response)
    page_state = PageConditionsState(
        takeoffZones=[zone_state]
    )

    return page_state
