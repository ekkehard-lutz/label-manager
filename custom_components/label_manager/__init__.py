"""The Label Manager integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS
from .label_sync import async_setup_device_listener
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

    hass.data[DOMAIN][entry.entry_id] = {
        "storage": storage,
        "unsubscribe": unsubscribe,
    }

    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS,
    )

    return True


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

    return await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )
