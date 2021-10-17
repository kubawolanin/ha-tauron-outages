"""Sample API Client."""
from __future__ import annotations

import asyncio
import socket
from typing import Any
import ssl

import aiohttp
import async_timeout
from requests import adapters
from urllib3 import poolmanager

from .const import LOGGER, REVERSE_GEOCODE_URL, POWER_URL

API_HEADERS = {aiohttp.hdrs.CONTENT_TYPE: "application/json; charset=UTF-8"}


class ApiClientException(Exception):
    """Api Client Exception."""


class TauronOutagesApiClient:
    def __init__(
        self,
        latitude: float,
        longitude: float,
        session: aiohttp.ClientSession,
    ) -> None:
        """Sample API Client."""
        self._latitude = latitude
        self._longitude = longitude
        self._session = session

    async def async_get_reverse_geocode(self) -> dict[str, Any]:
        """Get reverse geocode (address, postcode etc)."""
        geocode_url = (
            f"{REVERSE_GEOCODE_URL}&lat={self._latitude}&lon={self._longitude}"
        )
        return await self.api_wrapper("get", geocode_url)

    async def async_get_city_gaid(self, reverse_geocode) -> dict[str, Any]:
        """Get City Gaid"""
        postcode = reverse_geocode.get("address").get("postcode")
        get_cities_url = f"https://jsonplaceholder.typicode.com/posts/1"
        # get_cities_url = f"{POWER_URL}city/GetCities?partName={postcode}"
        return await self.api_wrapper("get", get_cities_url)

    async def async_get_street_gaid(self, reverse_geocode, city_gaid) -> dict[str, Any]:
        """Get Street Gaid"""
        road = reverse_geocode.get("address").get("road")

        get_streets_url = (
            f"{POWER_URL}street/GetStreets?ownerGaid={city_gaid}&partName={road}"
        )
        return await self.api_wrapper("get", get_streets_url)

    async def async_get_data(self, street_gaid) -> dict[str, Any]:
        """Get data from the Outages API."""
        get_outages_url = f"{POWER_URL}outage/GetOutages?gaid={street_gaid}&type=street"
        return await self.api_wrapper("get", get_outages_url)

    async def api_wrapper(
        self,
        method: str,
        url: str,
        data: dict[str, Any] = {},
        headers: dict = {"cache-control": "no-cache"},
    ) -> dict[str, Any] | None:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10, loop=asyncio.get_event_loop()):
                sslcontext = ssl.create_default_context()
                sslcontext.set_ciphers("DEFAULT@SECLEVEL=1")
                sslcontext.check_hostname = False
                LOGGER.info(url)
                response = await self._session.request(
                    method=method, url=url, headers=headers, json=data, ssl=sslcontext
                )
                if method == "get":
                    return await response.json()

        except asyncio.TimeoutError as exception:
            raise ApiClientException(
                f"Timeout error fetching information from {url}"
            ) from exception

        except (KeyError, TypeError) as exception:
            raise ApiClientException(
                f"Error parsing information from {url} - {exception}"
            ) from exception

        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise ApiClientException(
                f"Error fetching information from {url} - {exception}"
            ) from exception

        except Exception as exception:  # pylint: disable=broad-except
            raise ApiClientException(exception) from exception


# to fix the SSLError
class TLSAdapter(adapters.HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        """Create and initialize the urllib3 PoolManager."""
        ctx = ssl.create_default_context()
        ctx.set_ciphers("DEFAULT@SECLEVEL=1")
        ctx.check_hostname = False
        self.poolmanager = poolmanager.PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_version=ssl.PROTOCOL_TLS,
            ssl_context=ctx,
        )
