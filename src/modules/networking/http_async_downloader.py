from typing import Any, Dict

import aiofiles
from httpx import AsyncClient


class HttpAsyncDownloader:
    async def send_request(
        self,
        method: str,
        url: str,
        file_name: str,
        data: Dict[str, Any] | None = None,
        json: Dict[str, Any] | None = None,
        headers: Dict[str, str] | None = None,
        url_params: Dict[str, Any] | None = None,
    ):
        async with AsyncClient() as client:
            async with client.stream(
                method=method,
                url=url,
                data=data,
                json=json,
                headers=headers,
                params=url_params,
            ) as response:
                async with aiofiles.open(file_name, "wb") as f:
                    async for chunk in response.aiter_bytes():
                        if chunk:
                            await f.write(chunk)

    async def get_file_from_url(self, url: str, file_path: str):
        return await self.send_request("GET", url, file_path)
