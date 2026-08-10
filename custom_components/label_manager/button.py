"""Button platform for the Label Manager integration."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .label_sync import sync_all_devices


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities,
) -> None:
    """Set up the Label Manager button."""

    async_add_entities(
        [
            LabelManagerSyncButton(
                hass,
                entry,
            )
        ]
    )


class LabelManagerSyncButton(ButtonEntity):
    """Button to manually synchronize all device labels."""

    _attr_has_entity_name = True
    _attr_name = "Synchronize labels"
    _attr_icon = "mdi:sync"

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the synchronization button."""
        self.hass = hass
        self.entry = entry
        self._attr_unique_id = f"{entry.entry_id}_sync"

    async def async_press(self) -> None:
        """Synchronize labels for all registered devices."""
        storage = self.hass.data[DOMAIN][self.entry.entry_id]["storage"]

        await sync_all_devices(
            self.hass,
            storage,
        )
