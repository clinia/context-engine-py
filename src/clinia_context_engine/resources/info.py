# This file is auto-generated. Do not edit manually.
# Generated from the Context Engine OpenAPI spec.

from __future__ import annotations

from pydantic import TypeAdapter

from .._http import AsyncHttpClient, HttpClient
from ..generated.models import ServiceInfo

_SERVICE_INFO: TypeAdapter[ServiceInfo] = TypeAdapter(ServiceInfo)


class InfoResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def get_service_info(self) -> ServiceInfo:
        """Get service info.

        Returns the service name and the build identity of the running process. Use it to
        confirm which build a deployment is serving.
        """
        return self._http.request(
            "GET",
            "/",
            cast_to=_SERVICE_INFO,
        )


class AsyncInfoResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def get_service_info(self) -> ServiceInfo:
        """Get service info.

        Returns the service name and the build identity of the running process. Use it to
        confirm which build a deployment is serving.
        """
        return await self._http.request(
            "GET",
            "/",
            cast_to=_SERVICE_INFO,
        )
