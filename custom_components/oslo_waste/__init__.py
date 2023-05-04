"""Oslo Kommune, Avfall og gjenvinning"""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (
    CONF_LETTER,
    CONF_NUMBER,
    CONF_STREET,
    CONF_STREET_ID,
    DOMAIN,
    LOGGER,
    PLATFORMS,
    STARTUP_MESSAGE,
)
from .coordinator import OsloWasteCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Oslo Waste entry."""

    LOGGER.info(STARTUP_MESSAGE)
    hass.data.setdefault(DOMAIN, {})

    street = entry.data[CONF_STREET]
    number = entry.data.get(CONF_NUMBER, None)
    letter = entry.data.get(CONF_LETTER, None)
    street_id = entry.data.get(CONF_STREET_ID, None)

    coordinator = OsloWasteCoordinator(hass, street, number, letter, street_id)

    hass.data[DOMAIN][entry.entry_id] = coordinator

    hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
