from bleak import BleakClient, BLEDevice
from bleak_retry_connector import close_stale_connections, establish_connection
from .const import (
    FTMS_FITNESS_MACHINE_CONTROL_POINT_CHARACTERISTIC_UUID,
    FitnessMachineControlPointOperation,
    FitnessMachineStopCode,
)
import struct


class FitnessMachineDevice:
    _client: BleakClient
    _device: BLEDevice

    @property
    def rssi(self):
        pass

    @property
    def name(self):
        pass

    @property
    def address(self):
        pass

    @property
    def serial_number(self):
        pass

    @property
    def is_connected(self) -> bool:
        if self._client is None:
            return False

        return self._client.is_connected

    def __init__(self, ble_device: BLEDevice):
        self._device = ble_device
        self._client = None

    async def connect(self):
        if self.is_connected:
            return

        await close_stale_connections(self._device)

        self._client = await establish_connection(
            BleakClient, self._device, self._device.name
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
