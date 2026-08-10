import pytest
from unittest.mock import AsyncMock, MagicMock

from custom_components.label_manager import button


@pytest.mark.asyncio
async def test_sync_button(monkeypatch) -> None:
    """Pressing the button synchronizes all devices."""
    hass = MagicMock()
    entry = MagicMock()
    storage = MagicMock()

    entry.entry_id = "entry_123"

    hass.data = {
        "label_manager": {
            "entry_123": {
                "storage": storage,
            }
        }
    }

    sync_all_devices_mock = AsyncMock()

    monkeypatch.setattr(
        button,
        "sync_all_devices",
        sync_all_devices_mock,
    )

    sync_button = button.LabelManagerSyncButton(
        hass,
        entry,
    )

    await sync_button.async_press()

    sync_all_devices_mock.assert_awaited_once_with(
        hass,
        storage,
    )
