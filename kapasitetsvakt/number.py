from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN, CONF_MAX_KW, CONF_OFF_MARGIN, CONF_RECONNECT_MARGIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    data = {**entry.data, **entry.options}
    async_add_entities([
        KapasitetsvaktNumber(entry, CONF_MAX_KW, "Maks Kapasitetsledd", 1, 100, 1, "kW", "mdi:flash"),
        KapasitetsvaktNumber(entry, CONF_OFF_MARGIN, "Utkoblingsmargin", 0, 3, 0.1, "kW", "mdi:margin"),
        KapasitetsvaktNumber(entry, CONF_RECONNECT_MARGIN, "Gjeninnkoblingsmargin", 0, 3, 0.1, "kW", "mdi:margin"),
    ])

class KapasitetsvaktNumber(NumberEntity):
    def __init__(self, entry, key, name, min_val, max_val, step, unit, icon):
        self._entry = entry
        self._key = key
        self._attr_name = name
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._attr_native_min_value = min_val
        self._attr_native_max_value = max_val
        self._attr_native_step = step
        self._attr_native_unit_of_measurement = unit
        self._attr_icon = icon

    @property
    def native_value(self):
        return float(self._entry.options.get(self._key, self._entry.data.get(self._key, 0)))

    async def async_set_native_value(self, value: float) -> None:
        new_options = {**self._entry.options, self._key: value}
        self.hass.config_entries.async_update_entry(self._entry, options=new_options)