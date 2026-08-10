"""The Label Manager integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (
    CONF_AUTO_SYNC,
    CONF_SYNC_TIME,
    DEFAULT_AUTO_SYNC,
    DEFAULT_SYNC_TIME,
    DOMAIN,
    PLATFORMS,
)
from .label_sync import (
    async_setup_daily_sync,
    async_setup_device_listener,
)
from .storage import LabelManagerStorage


type LabelManagerConfigEntry = ConfigEntry


async def async_setup(
    hass: HomeAssistant,
    config: dict,
) -> bool:
    """Set up the Label Manager integration."""

    hass.data.setdefault(DOMAIN, {})

    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: LabelManagerConfigEntry,
) -> bool:
    """Set up Label Manager from a config entry."""

    hass.data.setdefault(DOMAIN, {})

    storage = LabelManagerStorage(hass)
    await storage.async_load()

    unsubscribe = await async_setup_device_listener(
        hass,
        storage,
    )

    daily_sync_unsubscribe = None

    if entry.options.get(
        CONF_AUTO_SYNC,
        DEFAULT_AUTO_SYNC,
    ):
        daily_sync_unsubscribe = async_setup_daily_sync(
            hass,
            storage,
            entry.options.get(
                CONF_SYNC_TIME,
                DEFAULT_SYNC_TIME,
            ),
        )

    hass.data[DOMAIN][entry.entry_id] = {
        "storage": storage,
        "unsubscribe": unsubscribe,
        "daily_sync_unsubscribe": daily_sync_unsubscribe,
    }

    entry.async_on_unload(
        entry.add_update_listener(_async_update_options)
    )

    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS,
    )

    return True


async def _async_update_options(
    hass: HomeAssistant,
    entry: LabelManagerConfigEntry,
) -> None:
    """Update the daily synchronization scheduler."""

    entry_data = hass.data[DOMAIN][entry.entry_id]

    old_daily_sync_unsubscribe = entry_data.get(
        "daily_sync_unsubscribe"
    )

    if old_daily_sync_unsubscribe is not None:
        old_daily_sync_unsubscribe()

    daily_sync_unsubscribe = None

    if entry.options.get(
        CONF_AUTO_SYNC,
        DEFAULT_AUTO_SYNC,
    ):
        daily_sync_unsubscribe = async_setup_daily_sync(
            hass,
            entry_data["storage"],
            entry.options.get(
                CONF_SYNC_TIME,
                DEFAULT_SYNC_TIME,
            ),
        )

    entry_data["daily_sync_unsubscribe"] = daily_sync_unsubscribe


async def async_unload_entry(
    hass: HomeAssistant,
    entry: LabelManagerConfigEntry,
) -> bool:
    """Unload a Label Manager config entry."""

    entry_data = hass.data[DOMAIN].pop(entry.entry_id, None)

    if entry_data is None:
        return True

    unsubscribe = entry_data.get("unsubscribe")

    if unsubscribe is not None:
        unsubscribe()

    daily_sync_unsubscribe = entry_data.get(
        "daily_sync_unsubscribe"
    )

    if daily_sync_unsubscribe is not None:
        daily_sync_unsubscribe()

    return await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )
