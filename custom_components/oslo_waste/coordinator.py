"""Data update coordinator for Oslo Waste."""

from typing import List
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from custom_components.oslo_waste.models import (
    HentePunkt,
    ResponseData,
    ResponseResult,
    Tjeneste,
)


from .api import OsloWasteApi
from .const import LOGGER


class OsloWasteCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from API."""

    addresses: List[ResponseResult]

    def __init__(
        self,
        hass: HomeAssistant,
        street: str or None,
        number: str or None,
        letter: str or None,
        street_id: str or None,
    ):
        self.hass = hass
        self.api = OsloWasteApi(async_get_clientsession(hass))

        self.street = street
        self.number = number
        self.letter = letter
        self.street_id = street_id

    async def async_update(self):
        data = ResponseData.from_dict(
            await self.api.fetch(self.street, self.number, self.letter, self.street_id)
        )
        self.addresses = data.results
