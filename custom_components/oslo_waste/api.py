import aiohttp
import async_timeout

from .const import BASEURL, CONF_STREET


class OsloWasteApi:
    """Oslo Waste API."""

    def __init__(self, session: aiohttp.ClientSession) -> None:
        """Initialize."""
        self._session = session

    async def fetch(self, street, number, letter, street_id) -> str:
        """Fetch from api."""

        url = BASEURL

        if street is not None:
            url += f"&street={street}"
        if number is not None:
            url += f"&number={number}"
        if letter is not None:
            url += f"&letter={letter}"
        if street_id is not None:
            url += f"&street_id={street_id}"

        with async_timeout.timeout(10):
            req = await self._session.get(url)

        return await req.json()
