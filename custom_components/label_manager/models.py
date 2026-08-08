"""Data models for the Label Manager integration."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class EntityLabelState:
    """Track labels managed by Label Manager for one entity."""

    entity_id: str
    device_id: str | None = None
    inherited_labels: set[str] = field(default_factory=set)


@dataclass(slots=True)
class DeviceLabelState:
    """Track the labels currently assigned to one device."""

    device_id: str
    labels: set[str] = field(default_factory=set)
    entity_ids: set[str] = field(default_factory=set)
