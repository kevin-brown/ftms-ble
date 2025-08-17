from typing import Any

from .const import DATA_FIELDS_TO_SUPPORTED_FEATURES, FitnessMachineDataField, FitnessMachineFeature
from .events import PropertyChangedEvent


class FitnessMachineData(dict[FitnessMachineDataField, int]):

    def __init__(self, supported_features: FitnessMachineFeature, on_change: callable[PropertyChangedEvent]):
        self._supported_features = supported_features

    def __setitem__(self, prop: FitnessMachineDataField, value: int):
        if feature_for_property := DATA_FIELDS_TO_SUPPORTED_FEATURES[prop]:
            if ~(self._supported_features & feature_for_property):
                raise KeyError(prop.name)

        super.__setitem__(prop, value)

    def update_supported_features(self, supported_feature: FitnessMachineFeature):
        self._supported_features = supported_feature
