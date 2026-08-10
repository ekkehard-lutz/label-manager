"""Constants for the Label Manager integration."""

from __future__ import annotations

from datetime import timedelta

DOMAIN = "label_manager"
NAME = "Label Manager"
VERSION = "0.0.1"

STORAGE_VERSION = 1
STORAGE_KEY = DOMAIN

PLATFORMS: list[str] = ["button"]

SYNC_INTERVAL = timedelta(days=1)
