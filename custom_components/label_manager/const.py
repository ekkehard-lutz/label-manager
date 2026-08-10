"""Constants for the Label Manager integration."""

from __future__ import annotations

from datetime import timedelta

DOMAIN = "label_manager"
NAME = "Label Manager"

STORAGE_VERSION = 1
STORAGE_KEY = DOMAIN

PLATFORMS: list[str] = ["button"]

SYNC_INTERVAL = timedelta(days=1)
CONF_SYNC_TIME = "sync_time"
DEFAULT_SYNC_TIME = "03:00:00"

CONF_AUTO_SYNC = "auto_sync"
DEFAULT_AUTO_SYNC = True
