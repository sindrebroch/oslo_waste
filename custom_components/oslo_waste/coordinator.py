"""Data update coordinator for Oslo Waste."""

from datetime import datetime
from bs4 import BeautifulSoup
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import OsloWasteApi
from .const import LOGGER


class OsloWasteCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from API."""

    def __init__(
        self,
        hass: HomeAssistant,
        address: str,
    ):
        self.hass = hass
        self.address = address
        self.api = OsloWasteApi(async_get_clientsession(hass))
        self._wastes = {}

    async def async_update(self):
        result = await self.api.fetch(self.address)

        LOGGER.debug("updating result %s", result)

        data = BeautifulSoup(result, "html.parser")

        LOGGER.debug("updating data %s", data)

        values = data.find("caption", text=self.address.upper())
        for v in values:
            root = v.parent.parent
            for w in root.select("tbody tr"):
                strings = w.select("td")
                self._wastes[strings[0].text] = {
                    "date": datetime.strptime(
                        strings[1].text.split(" ")[1], "%d.%m.%Y"
                    ).date(),
                    "frequency": strings[2].text,
                }

    async def waste_types(self) -> list[str]:
        return self._wastes.keys()

    async def get_waste(self, waste):
        return self._wastes[waste]
