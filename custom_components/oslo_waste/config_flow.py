import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.config_entries import ConfigFlow
from homeassistant.data_entry_flow import FlowResult

from .const import CONF_ADDRESS, DOMAIN

CONFIG_SCHEMA = vol.Schema({vol.Required(CONF_ADDRESS): cv.string})


class OsloWasteFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle a flow started by a user."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict[str, str] or None = None,
    ) -> FlowResult:
        """Flow."""

        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=CONFIG_SCHEMA,
                errors={},
                last_step=False,
            )

        return self.async_create_entry(
            title="Oslo waste",
            data=user_input,
        )