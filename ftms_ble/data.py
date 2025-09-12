from collections.abc import Callable
from typing import Any

from .const import DATA_FIELDS_TO_SUPPORTED_FEATURES, FitnessMachineDataField, FitnessMachineFeature
from .events import DataChangedEvent


class FitnessMachineData(dict[FitnessMachineDataField, int]):

    def __init__(self, supported_features: FitnessMachineFeature, on_change: Callable[[DataChangedEvent], None]):
        self._supported_features = supported_features
        self._on_change = on_change

    def __setitem__(self, prop: FitnessMachineDataField, value: int):
        if feature_for_property := DATA_FIELDS_TO_SUPPORTED_FEATURES[prop]:
            if ~(self._supported_features & feature_for_property):
                raise KeyError(prop.name)

        old_value = self[prop]

        super.__setitem__(prop, value)

        if old_value != value:
            event = DataChangedEvent(
                type="property_changed",
                data_field=prop,
                old_value=old_value,
                new_value=value,
            )
            self._on_change(event)

    def update_supported_features(self, supported_feature: FitnessMachineFeature):
        self._supported_features = supported_feature
