import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
    CONF_EFFECT_SENSOR,
    CONF_HOUR_SENSOR,
    CONF_NET_EFFECT_SENSOR,
    CONF_MAX_KW,
    CONF_OFF_MARGIN,
    CONF_RECONNECT_MARGIN,
    CONF_LOAD_COUNT,
    DEFAULT_MAX_KW,
    DEFAULT_OFF_MARGIN,
    DEFAULT_RECONNECT_MARGIN,
)

class KapasitetsvaktConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            self.data = user_input
            return await self.async_step_loads()

        schema = vol.Schema(
            {
                vol.Required(CONF_EFFECT_SENSOR): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor")
                ),
                vol.Required(CONF_HOUR_SENSOR): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor")
                ),
                vol.Optional(CONF_NET_EFFECT_SENSOR): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor")
                ),
                vol.Required(CONF_LOAD_COUNT, default=3): selector.NumberSelector(
                    selector.NumberSelectorConfig(min=1, max=6, mode=selector.NumberSelectorMode.BOX)
                ),
                vol.Required(CONF_MAX_KW, default=DEFAULT_MAX_KW): selector.NumberSelector(
                    selector.NumberSelectorConfig(min=1, max=100, step=1, unit_of_measurement="kW")
                ),
                vol.Required(CONF_OFF_MARGIN, default=DEFAULT_OFF_MARGIN): selector.NumberSelector(
                    selector.NumberSelectorConfig(min=0, max=3, step=0.1, unit_of_measurement="kW")
                ),
                vol.Required(CONF_RECONNECT_MARGIN, default=DEFAULT_RECONNECT_MARGIN): selector.NumberSelector(
                    selector.NumberSelectorConfig(min=0, max=3, step=0.1, unit_of_measurement="kW")
                ),
            }
        )

        return self.async_show_form(step_id="user", data_schema=schema)

    async def async_step_loads(self, user_input=None):
        if user_input is not None:
            self.data.update(user_input)
            return self.async_create_entry(title="Kapasitetsvakt", data=self.data)

        load_count = int(self.data.get(CONF_LOAD_COUNT, 3))
        fields = {}
        for i in range(1, load_count + 1):
            fields[vol.Required(f"load_{i}_entity")] = selector.EntitySelector(
                selector.EntitySelectorConfig()
            )

        return self.async_show_form(step_id="loads", data_schema=vol.Schema(fields))

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return KapasitetsvaktOptionsFlow(config_entry)


class KapasitetsvaktOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data = {**self.config_entry.data, **self.config_entry.options}
        schema = vol.Schema(
            {
                vol.Required(CONF_MAX_KW, default=data.get(CONF_MAX_KW, DEFAULT_MAX_KW)): selector.NumberSelector(
                    selector.NumberSelectorConfig(min=1, max=100, step=1, unit_of_measurement="kW")
                ),
                vol.Required(CONF_OFF_MARGIN, default=data.get(CONF_OFF_MARGIN, DEFAULT_OFF_MARGIN)): selector.NumberSelector(
                    selector.NumberSelectorConfig(min=0, max=3, step=0.1, unit_of_measurement="kW")
                ),
                vol.Required(
                    CONF_RECONNECT_MARGIN, default=data.get(CONF_RECONNECT_MARGIN, DEFAULT_RECONNECT_MARGIN)
                ): selector.NumberSelector(
                    selector.NumberSelectorConfig(min=0, max=3, step=0.1, unit_of_measurement="kW")
                ),
            }
        )

        return self.async_show_form(step_id="init", data_schema=schema)