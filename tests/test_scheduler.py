from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.label_manager import label_sync


@pytest.mark.asyncio
async def test_async_setup_daily_sync(monkeypatch) -> None:
    """Set up the daily synchronization at the configured time."""
    hass = MagicMock()
    storage = MagicMock()

    sync_all_devices = AsyncMock()
    monkeypatch.setattr(
        label_sync,
        "sync_all_devices",
        sync_all_devices,
    )

    async_track_time_change = MagicMock()
    monkeypatch.setattr(
        label_sync,
        "async_track_time_change",
        async_track_time_change,
    )

    unsubscribe = MagicMock()
    async_track_time_change.return_value = unsubscribe

    result = label_sync.async_setup_daily_sync(
        hass,
        storage,
        "11:30:45",
    )

    assert result is unsubscribe

    async_track_time_change.assert_called_once()

    call = async_track_time_change.call_args
    assert call.args[0] is hass
    assert call.kwargs["hour"] == 11
    assert call.kwargs["minute"] == 30
    assert call.kwargs["second"] == 45

    callback = call.args[1]

    await callback(None)

    sync_all_devices.assert_awaited_once_with(
        hass,
        storage,
    )
