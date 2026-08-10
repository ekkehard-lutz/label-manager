"""Config flow for the Label Manager integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector

from .const import (
    CONF_AUTO_SYNC,
    CONF_SYNC_TIME,
    DEFAULT_AUTO_SYNC,
    DEFAULT_SYNC_TIME,
    DOMAIN
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a Label Manager config flow."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        """Handle the initial setup step."""

        if user_input is not None:
            return self.async_create_entry(
                title="Label Manager",
                data={},
            )

        return self.async_show_form(
            step_id="user",
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""

        return OptionsFlowHandler()


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle Label Manager options."""

    async def async_step_init(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        """Manage Label Manager options."""

        if user_input is not None:
            return self.async_create_entry(data=user_input)

        current_auto_sync = self.config_entry.options.get(
            CONF_AUTO_SYNC,
            DEFAULT_AUTO_SYNC,
        )

        current_sync_time = self.config_entry.options.get(
            CONF_SYNC_TIME,
            DEFAULT_SYNC_TIME,
        )

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_AUTO_SYNC,
                        default=current_auto_sync,
                    ): selector.BooleanSelector(),

                    vol.Required(
                        CONF_SYNC_TIME,
                        default=current_sync_time,
                    ): selector.TimeSelector(
                        selector.TimeSelectorConfig(
                            format="24",
                        )
                    ),
                }
            ),
        )
