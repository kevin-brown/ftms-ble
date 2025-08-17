from typing import Literal, NamedTuple

from .const import FitnessMachineDataField, FitnessMachineStatusCode


class FitnessMachineEvent(NamedTuple):
    type: str


class DataChangedEvent(FitnessMachineEvent):
    type: Literal["property_changed"]
    data_field: FitnessMachineDataField
    old_value: int
    new_value: int


class FitnessMachineStatusChanged(FitnessMachineEvent):
    type: Literal["status_changed"]
    data_field: Literal["status"]
    old_value: FitnessMachineStatusCode
    new_value: FitnessMachineStatusCode
