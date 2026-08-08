"""Label inheritance synchronization."""

from __future__ import annotations

from dataclasses import dataclass

from collections.abc import Callable

from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import (
    async_track_device_registry_updated_event,
)
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.device_registry import EVENT_DEVICE_REGISTRY_UPDATED

from .services import get_device_entities, get_device_labels
from .storage import LabelManagerStorage


@dataclass(slots=True)
class LabelSyncResult:
    """Result of a label synchronization."""

    entity_labels: set[str]
    inherited_labels: set[str]
    labels_to_add: set[str]
    labels_to_remove: set[str]


def calculate_entity_labels(
    *,
    entity_labels: set[str],
    device_labels: set[str],
    inherited_labels: set[str],
) -> LabelSyncResult:
    """Calculate the label changes required for one entity.

    ``inherited_labels`` contains the labels that Label Manager currently
    considers inherited for this entity.

    Device labels are authoritative for inherited labels.

    Existing labels that are not known as inherited remain untouched.
    """

    # Labels which are currently inherited must be removed from the entity
    # if they no longer exist on the device.
    labels_to_remove = inherited_labels - device_labels

    # Every device label must exist on the entity.
    labels_to_add = device_labels - entity_labels

    # The resulting inherited-label state is exactly the current device
    # labels.
    new_inherited_labels = set(device_labels)

    new_entity_labels = (
        entity_labels
        - labels_to_remove
    ) | labels_to_add

    return LabelSyncResult(
        entity_labels=new_entity_labels,
        inherited_labels=new_inherited_labels,
        labels_to_add=labels_to_add,
        labels_to_remove=labels_to_remove,
    )


async def sync_entity(
    hass: HomeAssistant,
    storage: LabelManagerStorage,
    entity_id: str,
    device_id: str,
) -> LabelSyncResult:
    """Synchronize inherited labels for one entity."""

    entity_registry = er.async_get(hass)
    entity = entity_registry.async_get(entity_id)

    if entity is None:
        storage.remove_entity(entity_id)
        await storage.async_save()

        return LabelSyncResult(
            entity_labels=set(),
            inherited_labels=set(),
            labels_to_add=set(),
            labels_to_remove=set(),
        )

    current_entity_labels = set(entity.labels)
    current_device_labels = get_device_labels(hass, device_id)
    current_inherited_labels = storage.get_inherited_labels(entity_id)

    result = calculate_entity_labels(
        entity_labels=current_entity_labels,
        device_labels=current_device_labels,
        inherited_labels=current_inherited_labels,
    )

    new_labels = (
        current_entity_labels
        | result.labels_to_add
    ) - result.labels_to_remove

    if new_labels != current_entity_labels:
        entity_registry.async_update_entity(
            entity_id,
            labels=new_labels,
        )

    storage.set_inherited_labels(
        entity_id,
        result.inherited_labels,
    )

    return result


async def sync_device(
    hass: HomeAssistant,
    storage: LabelManagerStorage,
    device_id: str,
) -> dict[str, LabelSyncResult]:
    """Synchronize all entities belonging to a device."""

    results: dict[str, LabelSyncResult] = {}

    entity_ids = get_device_entities(hass, device_id)

    for entity_id in entity_ids:
        results[entity_id] = await sync_entity(
            hass,
            storage,
            entity_id,
            device_id,
        )

    await storage.async_save()

    return results


async def async_setup_device_listener(
    hass: HomeAssistant,
    storage: LabelManagerStorage,
) -> Callable[[], None]:
    """Listen for device registry changes."""

    async def _device_registry_updated(event_data) -> None:
        """Handle a device registry update."""

        changes = event_data.get("changes", {})

        if "labels" not in changes:
            return

        device_id = event_data["device_id"]

        await sync_device(
            hass,
            storage,
            device_id,
        )

    return hass.bus.async_listen(
        EVENT_DEVICE_REGISTRY_UPDATED,
        _device_registry_updated,
    )
