"""Persistent storage for the Label Manager integration."""

from __future__ import annotations

from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

from .const import STORAGE_KEY, STORAGE_VERSION


class LabelManagerStorage:
    """Persistent storage for Label Manager state."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the storage."""
        self.hass = hass
        self._store = Store[dict[str, Any]](
            hass,
            STORAGE_VERSION,
            STORAGE_KEY,
        )

        self._data: dict[str, Any] = {
            "version": STORAGE_VERSION,
            "entities": {},
        }

    async def async_load(self) -> None:
        """Load stored data from Home Assistant."""
        data = await self._store.async_load()

        if not data:
            return

        self._data = {
            "version": data.get("version", STORAGE_VERSION),
            "entities": data.get("entities", {}),
        }

    async def async_save(self) -> None:
        """Save current data to Home Assistant."""
        await self._store.async_save(self._data)

    def get_inherited_labels(self, entity_id: str) -> set[str]:
        """Return labels currently considered inherited for an entity."""
        entity_data = self._data["entities"].get(entity_id, {})

        return set(entity_data.get("inherited_labels", []))

    def set_inherited_labels(
        self,
        entity_id: str,
        labels: set[str],
    ) -> None:
        """Set the inherited labels for an entity."""
        if labels:
            self._data["entities"][entity_id] = {
                "inherited_labels": sorted(labels),
            }
        else:
            self._data["entities"].pop(entity_id, None)

    def remove_entity(self, entity_id: str) -> None:
        """Remove an entity from the stored state."""
        self._data["entities"].pop(entity_id, None)

    def get_all_entities(self) -> dict[str, set[str]]:
        """Return all entities and their inherited labels."""
        return {
            entity_id: set(entity_data.get("inherited_labels", []))
            for entity_id, entity_data in self._data["entities"].items()
        }
