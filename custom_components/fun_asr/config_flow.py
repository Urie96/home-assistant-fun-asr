import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.config_entries import ConfigFlow
from typing import Any, Dict, Optional
from homeassistant.data_entry_flow import FlowResult
import logging

from . import DOMAIN

MODELS = ["tiny", "small", "base", "medium", "large-v3"]

_LOGGER = logging.getLogger(__name__)


class ConfigFlowHandler(ConfigFlow, domain=DOMAIN):
    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        errors: Dict[str, str] = {}
        if user_input:
            return self.async_create_entry(title="Fun Asr", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("server"): str,
                    vol.Optional("model", default="base"): vol.In(MODELS),
                },
            ),
            errors=errors,
        )
