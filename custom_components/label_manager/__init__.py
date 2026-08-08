"""The Label Manager integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

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

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: LabelManagerConfigEntry,
) -> bool:
    """Unload a config entry."""

    return True
