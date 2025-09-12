from collections import defaultdict
from collections.abc import Callable
from ftms_ble.const import FTMS_FITNESS_MACHINE_FEATURE_CHARACTERISTIC_UUID


class MockBLEDevice:
    
    def __init__(self, name, address):
        self.name = name
        self.address = address

class MockBLEClient:
    
    def __init__(self, device):
        self._reads = []
        self._writes = []

        self._device = device

        self._characteristics = {
            FTMS_FITNESS_MACHINE_FEATURE_CHARACTERISTIC_UUID: bytearray()
        }
        self._responses = defaultdict(dict)
        self._notify_callbacks = defaultdict(list)

    def set_characteristic_data(self, characteristics: dict[str, bytearray]):
        self._characteristics.update(characteristics)
    
    def set_characteristic_responses(self, characteristic: str, responses: list[bytearray]):
        self._responses[characteristic] = responses

    def notify_characteristic(self, characteristic: str, data: bytearray):
        print(self._notify_callbacks)
        for callback in self._notify_callbacks[characteristic]:
            callback(self, data)

    async def read_gatt_char(self, characteristic: str):
        self._reads.append(characteristic)

        return self._characteristics[characteristic]

    async def write_gatt_char(self, characteristic: str, data: bytearray, response: bool = False):
        self._writes.append((characteristic, data, response))

        if response:
            return self._responses[characteristic][data]

    async def start_notify(self, characteristic: str, callback: Callable):
        self._notify_callbacks[characteristic].append(callback)
