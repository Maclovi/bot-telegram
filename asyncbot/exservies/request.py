from typing import Any

import aiohttp

from ..data.settings import secrets


async def ping_message(data: dict[str, Any]) -> str:
    conf_session = aiohttp.ClientSession(
        base_url=secrets.HOST_ASYNCLIENT,
        connector=aiohttp.TCPConnector(ssl=False),
        timeout=aiohttp.ClientTimeout(total=15),
    )
    try:
        async with conf_session as session:
            async with session.post('/pong_message', json=data) as response:
                if response.status == 202:
                    js: dict = await response.json()
                    return js["time"]
    except (TimeoutError, Exception) as e:
        print("err: a long wait", e)

    return ""
