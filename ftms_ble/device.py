from bleak import BleakClient, BLEDevice
from bleak_retry_connector import close_stale_connections, establish_connection
from collections.abc import Callable
from .const import (
    FTMS_FITNESS_MACHINE_CONTROL_POINT_CHARACTERISTIC_UUID,
    FTMS_FITNESS_MACHINE_FEATURE_CHARACTERISTIC_UUID,
    FTMS_FITNESS_MACHINE_STATUS_CHARACTERISTIC_UUID,
    FitnessMachineControlPointOperation,
    FitnessMachineDataField,
    FitnessMachineFeature,
    FitnessMachineStatusCode,
    FitnessMachineStopCode,
    FitnessMachineTargetSettingFeature,
)
from .data import FitnessMachineData
from .events import DataChangedEvent, FitnessMachineEvent, FitnessMachineStatusChanged
import logging
import struct

LOGGER = logging.getLogger(__name__)


class FitnessMachineDevice:
    _client: BleakClient
    _device: BLEDevice

    _features: FitnessMachineFeature
    _settings: FitnessMachineTargetSettingFeature

    _data: FitnessMachineData
    _properties_ranges: dict[FitnessMachineDataField, range]

    _status: FitnessMachineStatusCode

    @property
    def name(self):
        return self._device.name

    @property
    def address(self):
        return self._device.address

    @property
    def serial_number(self):
        pass

    @property
    def features(self):
        return self._features

    @property
    def settings(self):
        return self._settings

    @property
    def properties(self):
        return self._properties

    @property
    def is_connected(self) -> bool:
        if self._client is None:
            return False

        return self._client.is_connected

    @property
    def status(self) -> FitnessMachineStatusCode:
        return self._status

    def __init__(self, ble_device: BLEDevice, on_change: Callable[[FitnessMachineEvent], None]):
        self._device = ble_device
        self._client = None

        self._status = None

        self._features = FitnessMachineFeature(0)
        self._settings = FitnessMachineTargetSettingFeature(0)
        self._data = FitnessMachineData(self._features, self._on_data_change)

        self._on_change = on_change

    async def connect(self):
        if self.is_connected:
            return

        await close_stale_connections(self._device)

        self._client = await establish_connection(
            BleakClient, self._device, self._device.name
        )

        await self._update_features()

        await self._client.start_notify(
            FTMS_FITNESS_MACHINE_STATUS_CHARACTERISTIC_UUID,
            self._on_ftms_status_event,
        )

    async def disconnect(self):
        if not self.is_connected:
            return

        await self._client.disconnect()

    async def request_control(self):
        return await self._send_ftms_command(
            FitnessMachineControlPointOperation.REQUEST_CONTROL
        )

    async def start_resume(self):
        return await self._send_ftms_command(
            FitnessMachineControlPointOperation.START_OR_RESUME
        )

    async def stop_pause(self, stop_code: FitnessMachineStopCode):
        if stop_code == FitnessMachineStopCode.PAUSE:
            return await self.pause()
        elif stop_code == FitnessMachineStopCode.STOP:
            return await self.stop()

    async def stop(self):
        return await self._send_ftms_command(
            FitnessMachineControlPointOperation.STOP_OR_PAUSE,
            FitnessMachineStopCode.STOP,
        )

    async def pause(self):
        return await self._send_ftms_command(
            FitnessMachineControlPointOperation.STOP_OR_PAUSE,
            FitnessMachineStopCode.PAUSE,
        )

    async def reset(self):
        return await self._send_ftms_command(
            FitnessMachineControlPointOperation.RESET,
        )

    def _on_ftms_status_event(
        self, client: BleakClient, data: bytearray
    ):
        print("Fitness machine status: {}", data)

        status_code = FitnessMachineStatusCode(int.from_bytes(data[0:4], "little"))

        event = FitnessMachineStatusChanged(
            type="status_changed",
            data_field="status",
            old_value=self._status,
            new_value=status_code,
        )

        self._on_ftms_status_change(event)

    async def _send_ftms_command(
        self,
        operation: FitnessMachineControlPointOperation,
        parameters=None,
        response=True,
    ):
        await self.connect()

        command = struct.pack(">B", operation)
        if parameters:
            command_parameters = struct.pack(">B", parameters)
            command += command_parameters

        return await self._client.write_gatt_char(
            FTMS_FITNESS_MACHINE_CONTROL_POINT_CHARACTERISTIC_UUID,
            command,
            response=response,
        )

    def _trigger_on_change(self, event: FitnessMachineEvent):
        self._on_change(event)

    def _on_data_change(self, event: DataChangedEvent):
        self._trigger_on_change(event)

    def _on_ftms_status_change(self, event: FitnessMachineStatusChanged):
        self._trigger_on_change(event)

    async def _update_features(self):
        feature_data = await self._client.read_gatt_char(FTMS_FITNESS_MACHINE_FEATURE_CHARACTERISTIC_UUID)

        self._features = FitnessMachineFeature(int.from_bytes(feature_data[0:4], "little"))
        self._settings = FitnessMachineTargetSettingFeature(int.from_bytes(feature_data[4:8], "little"))

        self._data.update_supported_features(self._features)
