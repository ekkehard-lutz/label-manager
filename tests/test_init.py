from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.label_manager import (
    _async_update_options,
    async_setup_entry,
    async_unload_entry,
)
from custom_components.label_manager.const import (
    CONF_AUTO_SYNC,
    CONF_SYNC_TIME,
    DEFAULT_SYNC_TIME,
    DOMAIN,
)


@pytest.mark.asyncio
async def test_setup_entry_enables_daily_sync(monkeypatch) -> None:
    """Set up the daily sync when automatic synchronization is enabled."""
    hass = MagicMock()
    entry = MagicMock()
    entry.entry_id = "test_entry"
    entry.options = {
        CONF_AUTO_SYNC: True,
        CONF_SYNC_TIME: "11:30:00",
    }

    storage = MagicMock()
    storage.async_load = AsyncMock()

    monkeypatch.setattr(
        "custom_components.label_manager.LabelManagerStorage",
        lambda hass: storage,
    )

    device_listener_unsubscribe = MagicMock()
    monkeypatch.setattr(
        "custom_components.label_manager.async_setup_device_listener",
        AsyncMock(return_value=device_listener_unsubscribe),
    )

    daily_sync_unsubscribe = MagicMock()
    daily_sync_setup = MagicMock(return_value=daily_sync_unsubscribe)

    monkeypatch.setattr(
        "custom_components.label_manager.async_setup_daily_sync",
        daily_sync_setup,
    )

    hass.data = {}

    hass.config_entries.async_forward_entry_setups = AsyncMock(
        return_value=None,
    )

    result = await async_setup_entry(hass, entry)

    assert result is True

    daily_sync_setup.assert_called_once_with(
        hass,
        storage,
        "11:30:00",
    )

    assert hass.data[DOMAIN][entry.entry_id]["daily_sync_unsubscribe"] is (
        daily_sync_unsubscribe
    )


@pytest.mark.asyncio
async def test_setup_entry_disables_daily_sync(monkeypatch) -> None:
    """Do not set up the daily sync when automatic synchronization is disabled."""
    hass = MagicMock()
    entry = MagicMock()
    entry.entry_id = "test_entry"
    entry.options = {
        CONF_AUTO_SYNC: False,
        CONF_SYNC_TIME: DEFAULT_SYNC_TIME,
    }

    storage = MagicMock()
    storage.async_load = AsyncMock()

    monkeypatch.setattr(
        "custom_components.label_manager.LabelManagerStorage",
        lambda hass: storage,
    )

    device_listener_unsubscribe = MagicMock()
    monkeypatch.setattr(
        "custom_components.label_manager.async_setup_device_listener",
        AsyncMock(return_value=device_listener_unsubscribe),
    )

    daily_sync_setup = MagicMock()

    monkeypatch.setattr(
        "custom_components.label_manager.async_setup_daily_sync",
        daily_sync_setup,
    )

    hass.data = {}

    hass.config_entries.async_forward_entry_setups = AsyncMock(
        return_value=None,
    )

    result = await async_setup_entry(hass, entry)

    assert result is True

    daily_sync_setup.assert_not_called()

    assert hass.data[DOMAIN][entry.entry_id]["daily_sync_unsubscribe"] is None


@pytest.mark.asyncio
async def test_unload_entry_unsubscribes_daily_sync(monkeypatch) -> None:
    """Unload the integration and remove the daily sync listener."""
    hass = MagicMock()
    entry = MagicMock()
    entry.entry_id = "test_entry"

    device_listener_unsubscribe = MagicMock()
    daily_sync_unsubscribe = MagicMock()

    hass.data = {
        DOMAIN: {
            entry.entry_id: {
                "storage": MagicMock(),
                "unsubscribe": device_listener_unsubscribe,
                "daily_sync_unsubscribe": daily_sync_unsubscribe,
            }
        }
    }

    hass.config_entries.async_unload_platforms = AsyncMock(
        return_value=True,
    )

    result = await async_unload_entry(hass, entry)

    assert result is True

    device_listener_unsubscribe.assert_called_once()
    daily_sync_unsubscribe.assert_called_once()


@pytest.mark.asyncio
async def test_options_update_restarts_daily_sync(monkeypatch) -> None:
    """Restart the daily sync when the integration options change."""
    hass = MagicMock()
    entry = MagicMock()
    entry.entry_id = "test_entry"

    storage = MagicMock()

    old_daily_sync_unsubscribe = MagicMock()
    new_daily_sync_unsubscribe = MagicMock()

    daily_sync_setup = MagicMock(
        return_value=new_daily_sync_unsubscribe,
    )

    monkeypatch.setattr(
        "custom_components.label_manager.async_setup_daily_sync",
        daily_sync_setup,
    )

    hass.data = {
        DOMAIN: {
            entry.entry_id: {
                "storage": storage,
                "unsubscribe": MagicMock(),
                "daily_sync_unsubscribe": old_daily_sync_unsubscribe,
            }
        }
    }

    entry.options = {
        CONF_AUTO_SYNC: True,
        CONF_SYNC_TIME: "11:30:00",
    }

    await _async_update_options(hass, entry)

    old_daily_sync_unsubscribe.assert_called_once()

    daily_sync_setup.assert_called_once_with(
        hass,
        storage,
        "11:30:00",
    )

    assert (
        hass.data[DOMAIN][entry.entry_id]["daily_sync_unsubscribe"]
        is new_daily_sync_unsubscribe
    )


@pytest.mark.asyncio
async def test_update_options_restarts_daily_sync(monkeypatch) -> None:
    """Restart the daily sync when options change."""
    hass = MagicMock()
    entry = MagicMock()
    entry.entry_id = "test_entry"

    storage = MagicMock()

    old_daily_sync_unsubscribe = MagicMock()
    new_daily_sync_unsubscribe = MagicMock()

    daily_sync_setup = MagicMock(
        return_value=new_daily_sync_unsubscribe,
    )

    monkeypatch.setattr(
        "custom_components.label_manager.async_setup_daily_sync",
        daily_sync_setup,
    )

    hass.data = {
        DOMAIN: {
            entry.entry_id: {
                "storage": storage,
                "unsubscribe": MagicMock(),
                "daily_sync_unsubscribe": old_daily_sync_unsubscribe,
            }
        }
    }

    entry.options = {
        CONF_AUTO_SYNC: True,
        CONF_SYNC_TIME: "11:30:00",
    }

    await _async_update_options(hass, entry)

    old_daily_sync_unsubscribe.assert_called_once()

    daily_sync_setup.assert_called_once_with(
        hass,
        storage,
        "11:30:00",
    )

    assert (
        hass.data[DOMAIN][entry.entry_id]["daily_sync_unsubscribe"]
        is new_daily_sync_unsubscribe
    )


@pytest.mark.asyncio
async def test_setup_entry_registers_options_update_listener(
    monkeypatch,
) -> None:
    """Register an options update listener."""
    hass = MagicMock()
    entry = MagicMock()
    entry.entry_id = "test_entry"

    storage = MagicMock()
    storage.async_load = AsyncMock()

    monkeypatch.setattr(
        "custom_components.label_manager.LabelManagerStorage",
        lambda hass: storage,
    )

    monkeypatch.setattr(
        "custom_components.label_manager.async_setup_device_listener",
        AsyncMock(return_value=MagicMock()),
    )

    monkeypatch.setattr(
        "custom_components.label_manager.async_setup_daily_sync",
        MagicMock(return_value=MagicMock()),
    )

    hass.data = {}

    hass.config_entries.async_forward_entry_setups = AsyncMock(
        return_value=None,
    )

    listener_unsubscribe = MagicMock()

    entry.add_update_listener.return_value = listener_unsubscribe

    await async_setup_entry(hass, entry)

    entry.add_update_listener.assert_called_once_with(
        _async_update_options,
    )

    entry.async_on_unload.assert_called_once_with(
        listener_unsubscribe,
    )


@pytest.mark.asyncio
async def test_update_options_disables_daily_sync(monkeypatch) -> None:
    """Disable the daily sync when automatic synchronization is turned off."""
    hass = MagicMock()
    entry = MagicMock()
    entry.entry_id = "test_entry"

    storage = MagicMock()

    old_daily_sync_unsubscribe = MagicMock()

    daily_sync_setup = MagicMock()

    monkeypatch.setattr(
        "custom_components.label_manager.async_setup_daily_sync",
        daily_sync_setup,
    )

    hass.data = {
        DOMAIN: {
            entry.entry_id: {
                "storage": storage,
                "unsubscribe": MagicMock(),
                "daily_sync_unsubscribe": old_daily_sync_unsubscribe,
            }
        }
    }

    entry.options = {
        CONF_AUTO_SYNC: False,
        CONF_SYNC_TIME: "11:30:00",
    }

    await _async_update_options(hass, entry)

    old_daily_sync_unsubscribe.assert_called_once()
    daily_sync_setup.assert_not_called()

    assert (
        hass.data[DOMAIN][entry.entry_id]["daily_sync_unsubscribe"]
        is None
    )
