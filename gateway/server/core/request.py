from typing import Union, Optional

from aiohttp import ClientSession, JsonPayload
from async_timeout import timeout as _timeout
from starlette.datastructures import Headers

from server.utils.form import CustomFormData
from server.utils.response import decode_json
from server.utils.request import create_dict_if_not


async def fetch(
        url: str,
        method: str,
        headers: Union[Headers, dict],
        query_params: Optional[dict] = None,
        data: Union[CustomFormData, JsonPayload] = None,
        timeout: int = 60
):
    data = create_dict_if_not(data=data)
    query = create_dict_if_not(data=query_params)
    async with _timeout(delay=timeout):
        async with ClientSession(headers=headers) as session:
            async with session.request(
                    method=method,
                    url=url,
                    params=query,
                    data=data
            ) as response:
                response_json = await response.json()
                decoded_json = decode_json(data=response_json)
                return decoded_json, response.status, response.headers