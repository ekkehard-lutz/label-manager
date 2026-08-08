"""Tests for Label Manager label inheritance."""

import asyncio
import pytest
from custom_components.label_manager.label_sync import calculate_entity_labels
from unittest.mock import AsyncMock, MagicMock, patch


def test_new_device_label_is_inherited() -> None:
    """A new device label is added to the entity."""
    result = calculate_entity_labels(
        entity_labels=set(),
        device_labels={"Beleuchtung"},
        inherited_labels=set(),
    )

    assert result.entity_labels == {"Beleuchtung"}
    assert result.inherited_labels == {"Beleuchtung"}
    assert result.labels_to_add == {"Beleuchtung"}
    assert result.labels_to_remove == set()


def test_manual_entity_label_is_preserved() -> None:
    """Manual entity labels are preserved."""
    result = calculate_entity_labels(
        entity_labels={"Energie"},
        device_labels={"Beleuchtung"},
        inherited_labels=set(),
    )

    assert result.entity_labels == {"Energie", "Beleuchtung"}
    assert result.inherited_labels == {"Beleuchtung"}


def test_removed_device_label_is_removed() -> None:
    """An inherited label removed from the device is removed."""
    result = calculate_entity_labels(
        entity_labels={"Beleuchtung", "Energie"},
        device_labels=set(),
        inherited_labels={"Beleuchtung"},
    )

    assert result.entity_labels == {"Energie"}
    assert result.inherited_labels == set()
    assert result.labels_to_remove == {"Beleuchtung"}


def test_manual_label_becomes_inherited() -> None:
    """An existing entity label becomes inherited when the device gets it."""
    result = calculate_entity_labels(
        entity_labels={"Beleuchtung"},
        device_labels={"Beleuchtung"},
        inherited_labels=set(),
    )

    assert result.entity_labels == {"Beleuchtung"}
    assert result.inherited_labels == {"Beleuchtung"}
    assert result.labels_to_add == set()
    assert result.labels_to_remove == set()


def test_manually_readded_inherited_label_stays_inherited() -> None:
    """A manually re-added inherited label remains inherited."""
    result = calculate_entity_labels(
        entity_labels={"Beleuchtung"},
        device_labels={"Beleuchtung"},
        inherited_labels={"Beleuchtung"},
    )

    assert result.entity_labels == {"Beleuchtung"}
    assert result.inherited_labels == {"Beleuchtung"}


def test_only_removed_inherited_labels_are_removed() -> None:
    """Only obsolete inherited labels are removed."""
    result = calculate_entity_labels(
        entity_labels={"Beleuchtung", "Wohnzimmer", "Energie"},
        device_labels={"Wohnzimmer"},
        inherited_labels={"Beleuchtung", "Wohnzimmer"},
    )

    assert result.entity_labels == {"Wohnzimmer", "Energie"}
    assert result.inherited_labels == {"Wohnzimmer"}
    assert result.labels_to_add == set()
    assert result.labels_to_remove == {"Beleuchtung"}


def test_multiple_device_labels_are_inherited() -> None:
    """Multiple device labels are inherited."""
    result = calculate_entity_labels(
        entity_labels={"Energie"},
        device_labels={"Beleuchtung", "Wohnzimmer"},
        inherited_labels=set(),
    )

    assert result.entity_labels == {
        "Energie",
        "Beleuchtung",
        "Wohnzimmer",
    }
    assert result.inherited_labels == {
        "Beleuchtung",
        "Wohnzimmer",
    }


def test_manually_added_inherited_label_becomes_inherited() -> None:
    """A manually existing device label becomes inherited."""
    result = calculate_entity_labels(
        entity_labels={"Energie", "Beleuchtung"},
        device_labels={"Beleuchtung"},
        inherited_labels=set(),
    )

    assert result.entity_labels == {"Energie", "Beleuchtung"}
    assert result.inherited_labels == {"Beleuchtung"}
    assert result.labels_to_add == set()
    assert result.labels_to_remove == set()


def test_manually_restored_inherited_label_stays_inherited() -> None:
    """A manually restored inherited label remains inherited."""
    result = calculate_entity_labels(
        entity_labels={"Beleuchtung"},
        device_labels={"Beleuchtung"},
        inherited_labels={"Beleuchtung"},
    )

    assert result.entity_labels == {"Beleuchtung"}
    assert result.inherited_labels == {"Beleuchtung"}
    assert result.labels_to_add == set()
    assert result.labels_to_remove == set()


def test_removed_device_label_is_removed_from_entity() -> None:
    """A removed device label is removed from the entity."""
    result = calculate_entity_labels(
        entity_labels={"Energie", "Beleuchtung"},
        device_labels=set(),
        inherited_labels={"Beleuchtung"},
    )

    assert result.entity_labels == {"Energie"}
    assert result.inherited_labels == set()
    assert result.labels_to_add == set()
    assert result.labels_to_remove == {"Beleuchtung"}


def test_non_inherited_entity_label_is_not_removed() -> None:
    """A manually assigned entity label is preserved."""
    result = calculate_entity_labels(
        entity_labels={"Energie", "Beleuchtung"},
        device_labels=set(),
        inherited_labels=set(),
    )

    assert result.entity_labels == {"Energie", "Beleuchtung"}
    assert result.inherited_labels == set()
    assert result.labels_to_add == set()
    assert result.labels_to_remove == set()


def test_device_listener_syncs_on_label_change() -> None:
    """A device label change triggers synchronization."""

    hass = MagicMock()
    storage = MagicMock()

    with patch.object(hass.bus, "async_listen") as register_listener:
        from custom_components.label_manager.label_sync import (
            async_setup_device_listener,
        )

        register_listener.return_value = MagicMock()

        unsubscribe = asyncio.run(
            async_setup_device_listener(
                hass,
                storage,
            )
        )

        callback = register_listener.call_args.args[1]

        with patch(
            "custom_components.label_manager.label_sync.sync_device",
            new=AsyncMock(),
        ) as sync_device_mock:
            asyncio.run(
                callback(
                    {
                        "device_id": "device_123",
                        "action": "update",
                        "changes": {
                            "labels": {
                                "old": [],
                                "new": ["Beleuchtung"],
                            }
                        },
                    }
                )
            )

            sync_device_mock.assert_awaited_once_with(
                hass,
                storage,
                "device_123",
            )

        assert unsubscribe is register_listener.return_value


def test_device_listener_ignores_non_label_change() -> None:
    """A device change without label changes is ignored."""

    hass = MagicMock()
    storage = MagicMock()

    with patch.object(hass.bus, "async_listen") as register_listener:
        from custom_components.label_manager.label_sync import (
            async_setup_device_listener,
        )

        register_listener.return_value = MagicMock()

        asyncio.run(
            async_setup_device_listener(
                hass,
                storage,
            )
        )

        callback = register_listener.call_args.args[1]

        with patch(
            "custom_components.label_manager.label_sync.sync_device",
            new=AsyncMock(),
        ) as sync_device_mock:
            asyncio.run(
                callback(
                    {
                        "device_id": "device_123",
                        "action": "update",
                        "changes": {
                            "name": {
                                "old": "Shelly",
                                "new": "Shelly Dimmer",
                            }
                        },
                    }
                )
            )

            sync_device_mock.assert_not_awaited()


def test_device_label_replacement_is_applied() -> None:
    """A removed inherited label is replaced by a new device label."""

    result = calculate_entity_labels(
        entity_labels={"Energie", "Beleuchtung"},
        device_labels={"Beleuchtung innen"},
        inherited_labels={"Beleuchtung"},
    )

    assert result.entity_labels == {
        "Energie",
        "Beleuchtung innen",
    }

    assert result.inherited_labels == {
        "Beleuchtung innen",
    }

    assert result.labels_to_add == {
        "Beleuchtung innen",
    }

    assert result.labels_to_remove == {
        "Beleuchtung",
    }
