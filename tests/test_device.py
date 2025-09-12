from ftms_ble.const import FTMS_FITNESS_MACHINE_FEATURE_CHARACTERISTIC_UUID, FTMS_FITNESS_MACHINE_STATUS_CHARACTERISTIC_UUID, FitnessMachineStatusCode
from ftms_ble.device import FitnessMachineDevice
from ftms_ble.events import FitnessMachineStatusChanged
from tests.utils import MockBLEClient, MockBLEDevice
from unittest.mock import Mock
import pytest


@pytest.fixture()
def ble_device():
    return MockBLEDevice(
        name="Test FTMS",
        address="0:0:0",
    )

@pytest.fixture()
def ftms_device(ble_device):
    def on_change(event):
        device._events.append(event)

    device = FitnessMachineDevice(ble_device, on_change)
    device._events = []

    return device

@pytest.fixture()
def patch_establish_client(monkeypatch, ble_device):
    ble_client = MockBLEClient(
        device=ble_device,
    )

    async def establish_connection(client, device, name):
        return ble_client

    monkeypatch.setattr("ftms_ble.device.establish_connection", establish_connection)

    return ble_client

@pytest.mark.asyncio
async def test_connect_sets_notify(ftms_device, patch_establish_client):
    await ftms_device.connect()

    assert patch_establish_client._notify_callbacks[FTMS_FITNESS_MACHINE_STATUS_CHARACTERISTIC_UUID] != []


@pytest.mark.asyncio
async def test_ftms_status_event_parses_code(ftms_device, patch_establish_client):
    await ftms_device.connect()

    patch_establish_client.notify_characteristic(FTMS_FITNESS_MACHINE_STATUS_CHARACTERISTIC_UUID, b"\01")

    assert ftms_device._events == [FitnessMachineStatusChanged(
        type="status_changed",
        data_field="status",
        old_value=None,
        new_value=FitnessMachineStatusCode.RESET,
    )]
