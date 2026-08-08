"""Tests for Label Manager Home Assistant services."""

from unittest.mock import MagicMock

from custom_components.label_manager.services import get_device_entities


def test_get_device_entities(monkeypatch) -> None:
    """Return all entities belonging to a device."""
    hass = MagicMock()

    entity_registry = MagicMock()

    entity_registry.async_entries_for_device.return_value = [
        MagicMock(entity_id="light.test_light"),
        MagicMock(entity_id="sensor.test_power"),
        MagicMock(entity_id="sensor.test_energy"),
    ]

    from custom_components.label_manager import services

    monkeypatch.setattr(
        services.er,
        "async_get",
        lambda hass: entity_registry,
    )

    result = get_device_entities(hass, "device_123")

    assert result == {
        "light.test_light",
        "sensor.test_power",
        "sensor.test_energy",
    }

    entity_registry.async_entries_for_device.assert_called_once_with(
        "device_123",
        include_disabled_entities=True,
    )


