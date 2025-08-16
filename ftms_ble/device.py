from bleak import BleakClient, BLEDevice
from bleak_retry_connector import close_stale_connections, establish_connection
from .const import FitnessMachineStopCode


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

        self._client = await establish_connection(self._device)

    async def disconnect(self):
        if not self.is_connected:
            return

        await self._client.disconnect()

    async def start_resume(self):
        pass

    async def stop_pause(self, stop_code: FitnessMachineStopCode):
        if stop_code == FitnessMachineStopCode.PAUSE:
            return await self.pause()
        elif stop_code == FitnessMachineStopCode.STOP:
            return await self.stop()

    async def stop(self):
        pass

    async def pause(self):
        pass

    async def reset(self):
        pass
