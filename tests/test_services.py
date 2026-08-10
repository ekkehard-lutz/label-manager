"""Tests for Label Manager Home Assistant services."""

from unittest.mock import MagicMock

from custom_components.label_manager.services import get_device_entities


def test_get_device_entities(monkeypatch) -> None:
    """Return all entities belonging to a device."""
    hass = MagicMock()

    entity_registry = MagicMock()

    entity_registry.entities = {
        "light.test_light": MagicMock(
            entity_id="light.test_light",
            device_id="device_123",
        ),
        "sensor.test_power": MagicMock(
            entity_id="sensor.test_power",
            device_id="device_123",
        ),
        "sensor.test_energy": MagicMock(
            entity_id="sensor.test_energy",
            device_id="device_123",
        ),
        "sensor.other": MagicMock(
            entity_id="sensor.other",
            device_id="other_device",
        ),
    }

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


def test_get_device_ids(monkeypatch) -> None:
    """Return all registered device IDs."""
    hass = MagicMock()

    device_registry = MagicMock()
    device_registry.devices = {
        "device_123": MagicMock(),
        "device_456": MagicMock(),
        "device_789": MagicMock(),
    }

    from custom_components.label_manager import services

    monkeypatch.setattr(
        services.dr,
        "async_get",
        lambda hass: device_registry,
    )

    result = services.get_device_ids(hass)

    assert result == {
        "device_123",
        "device_456",
        "device_789",
    }
