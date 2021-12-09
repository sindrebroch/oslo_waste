import asyncio
import aiohttp
import async_timeout

from .const import BASEURL, CONF_STREET


class OsloWasteApi:
    def __init__(self, session: aiohttp.ClientSession) -> None:
        """Initialize."""
        self._session = session

    async def fetch(self, street) -> str:
        """Fetch from api."""

        with async_timeout.timeout(10):
            req = await self._session.get(
                BASEURL,
                params={CONF_STREET: street},
            )

        return await req.text()
