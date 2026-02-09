"""
Pydantic models for Takeoff Service API.
Based on OpenAPI specification schemas.
"""
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, computed_field


class Point(BaseModel):
    """2D coordinate point on the drawing."""
    x: float = Field(..., description="X coordinate (horizontal position)")
    y: float = Field(..., description="Y coordinate (vertical position)")


class NormalizedBoundingBoxModel(BaseModel):
    """Square area with coordinates in document that contain some object."""
    left: float = Field(..., description="Left bound coordinate")
    top: float = Field(..., description="Top bound coordinate")
    right: float = Field(..., description="Right bound coordinate")
    bottom: float = Field(..., description="Bottom bound coordinate")

    @computed_field
    @property
    def width(self) -> float:
        """Calculated width of the square."""
        return self.right - self.left

    @computed_field
    @property
    def height(self) -> float:
        """Calculated height of the square."""
        return self.bottom - self.top


class NameValuePair(BaseModel):
    """Generic key-value pair for properties and attributes."""
    name: Optional[str] = Field(None, description="Property/attribute name")
    value: Optional[str] = Field(None, description="Property/attribute value")


class QuantityDto(BaseModel):
    """Definition of a measurement quantity for a condition."""
    name: Optional[str] = Field(None, description="Quantity name (e.g., 'Count', 'Area', 'Length')")
    unitOfMeasure: Optional[str] = Field(None, description="Unit of measurement (e.g., 'ea', 'm²', 'm')")
    excludeAttachments: bool = Field(False, description="Whether to exclude attached items from this quantity")


class QuantityValue(BaseModel):
    """Actual measured value for a quantity."""
    name: Optional[str] = Field(None, description="Quantity name matching QuantityDto")
    unitOfMeasure: Optional[str] = Field(None, description="Unit of measurement")
    value: float = Field(..., description="Measured numeric value")


class TakeoffItemDto(BaseModel):
    """Specific measurement instance with coordinates on the drawing."""
    id: UUID = Field(..., description="Unique identifier of this takeoff item")
    conditionId: UUID = Field(..., description="Parent condition ID")
    takeoffZoneId: UUID = Field(..., description="Parent takeoff zone ID")
    parentTakeoffItemId: Optional[UUID] = Field(None, description="Parent item ID (for attachments)")
    points: Optional[List[Point]] = Field(None, description="Coordinate points defining the item geometry")
    angle: Optional[float] = Field(None, description="Rotation angle in degrees")
    itemName: Optional[str] = Field(None, description="Custom name for this specific item")
    quantityValues: Optional[List[QuantityValue]] = Field(None, description="Measured values for all quantities")


class ConditionDto(BaseModel):
    """Represents a type of construction element (Window, Door, Wall) with measurement rules."""
    id: UUID = Field(..., description="Unique identifier of the condition")
    name: Optional[str] = Field(None, description="Display name (e.g., 'Standard Window 1200x1500')")
    type: Optional[str] = Field(None, description="Measurement type - Count, Linear, Area")
    description: Optional[str] = Field(None, description="Additional notes about this condition")
    layer: Optional[str] = Field(None, description="Drawing layer name")
    color: Optional[str] = Field(None, description="Display color for UI")
    lineStyle: Optional[str] = Field(None, description="Line style for rendering")
    fillPattern: Optional[str] = Field(None, description="Fill pattern for area elements")
    isAttachment: bool = Field(False, description="Whether this is an attachment to another element")
    category: Optional[str] = Field(None, description="Category grouping (e.g., 'Doors', 'Windows')")
    shape: Optional[str] = Field(None, description="Geometric shape - Window, Column, Square, etc.")
    quantities: Optional[List[QuantityDto]] = Field(None, description="Measurement quantities defined for this condition")
    properties: Optional[List[NameValuePair]] = Field(None, description="Standard properties (key-value pairs)")
    customAttributes: Optional[List[NameValuePair]] = Field(None, description="User-defined custom attributes")


class ConditionState(BaseModel):
    """Complete state of a condition with all its measured items."""
    condition: Optional[ConditionDto] = Field(None, description="Condition definition")
    takeoffItems: Optional[List[TakeoffItemDto]] = Field(None, description="All measurement instances for this condition")


class TakeoffZoneDto(BaseModel):
    """Scaled region on the drawing with DPI and scale factor (e.g., 1:100)."""
    id: UUID = Field(..., description="Unique identifier of the zone")
    scale: float = Field(..., description="Scale factor (e.g., 100 for 1:100 scale)")
    name: Optional[str] = Field(None, description="Zone name (e.g., 'Floor Plan - Scale 1:100')")
    boundingBox: Optional[NormalizedBoundingBoxModel] = Field(None, description="Rectangular area defining the zone boundaries")
    dpi: int = Field(..., description="Dots per inch resolution of the drawing")


class TakeoffZoneState(BaseModel):
    """Complete state of a zone with all its conditions."""
    takeoffZone: Optional[TakeoffZoneDto] = Field(None, description="Zone metadata (scale, DPI, boundaries)")
    conditions: Optional[List[ConditionState]] = Field(None, description="All conditions measured within this zone")


class PageConditionsState(BaseModel):
    """Complete state of all takeoff zones and conditions for a document page."""
    takeoffZones: Optional[List[TakeoffZoneState]] = Field(None, description="All takeoff zones on this page with their conditions")
