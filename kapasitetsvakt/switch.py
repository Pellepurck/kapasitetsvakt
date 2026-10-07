from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    async_add_entities([KapasitetsvaktAktivSwitch(entry)])

class KapasitetsvaktAktivSwitch(SwitchEntity):
    def __init__(self, entry):
        self._entry = entry
        self._attr_name = "Kapasitetsvakt Aktiv"
        self._attr_unique_id = f"{entry.entry_id}_aktiv"
        self._attr_icon = "mdi:shield-check"
        self._is_on = True

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        self._is_on = False
        self.async_write_ha_state()