from bleak import BleakClient
from .const import FitnessMachineStopCode


class FitnessMachineDevice:

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

    def __init__(self, bluetooth_client: BleakClient):
        self.client = bluetooth_client

    async def connect(self):
        pass

    async def disconnect(self):
        pass

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
