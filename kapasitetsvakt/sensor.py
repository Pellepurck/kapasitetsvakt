from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN, CONF_MAX_KW, CONF_OFF_MARGIN, CONF_RECONNECT_MARGIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    data = {**entry.data, **entry.options}
    async_add_entities([
        KapasitetsvaktGrenseSensor(entry.entry_id, data),
        KapasitetsvaktUtkoblingsgrenseSensor(entry.entry_id, data)
    ])

class KapasitetsvaktGrenseSensor(SensorEntity):
    def __init__(self, entry_id, data):
        self._attr_name = "Kapasitetsvakt Grense"
        self._attr_unique_id = f"{entry_id}_grense"
        self._attr_native_unit_of_measurement = "kW"
        self._data = data

    @property
    def native_value(self):
        return float(self._data.get(CONF_MAX_KW, 5.0))

class KapasitetsvaktUtkoblingsgrenseSensor(SensorEntity):
    def __init__(self, entry_id, data):
        self._attr_name = "Kapasitetsvakt Utkoblingsgrense"
        self._attr_unique_id = f"{entry_id}_utkoblingsgrense"
        self._attr_native_unit_of_measurement = "kW"
        self._data = data

    @property
    def native_value(self):
        max_kw = float(self._data.get(CONF_MAX_KW, 5.0))
        off_margin = float(self._data.get(CONF_OFF_MARGIN, 0.3))
        return max(max_kw - off_margin, 0.0)