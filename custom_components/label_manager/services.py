"""Home Assistant services for the Label Manager integration."""

from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er


def get_device_entities(
    hass: HomeAssistant,
    device_id: str,
) -> set[str]:
    """Return all entity IDs belonging to a device."""

    entity_registry = er.async_get(hass)

    return {
        entity.entity_id
        for entity in entity_registry.entities.values()
        if entity.device_id == device_id
    }


def get_device_labels(
    hass: HomeAssistant,
    device_id: str,
) -> set[str]:
    """Return all labels currently assigned to a device."""
    device_registry = dr.async_get(hass)

    device = device_registry.async_get(device_id)

    if device is None:
        return set()

    return set(device.labels)


def get_device_ids(
    hass: HomeAssistant,
) -> set[str]:
    """Return all device IDs currently registered in Home Assistant."""
    device_registry = dr.async_get(hass)

    return set(device_registry.devices)
