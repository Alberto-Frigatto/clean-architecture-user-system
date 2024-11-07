from collections.abc import Callable
from http import HTTPStatus
from typing import Any

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_when_try_to_access_a_non_existent_endpoint_returns_NOT_FOUND(
    app_client: AsyncClient,
    is_datetime: Callable[[Any], bool],
) -> None:
    endpoint: str = '/non/existent'
    response = await app_client.get(endpoint)
    response_data: dict[str, Any] = response.json()

    assert response.status_code == HTTPStatus.NOT_FOUND

    assert is_datetime(response_data.pop('timestamp'))

    assert response_data == {
        'name': 'EndpointNotFound',
        'scope': 'ApiGeneralException',
        'type': 'NotFound',
        'message': f'The endpoint {endpoint} doesn\'t exists',
        'status': HTTPStatus.NOT_FOUND,
    }


@pytest.mark.asyncio
async def test_when_try_to_access_an_endpoint_with_method_not_allowed_returns_METHOD_NOT_ALLOWED(
    app_client: AsyncClient,
    is_datetime: Callable[[Any], bool],
) -> None:
    method: str = 'GET'
    endpoint: str = '/users/'
    response = await getattr(app_client, method.lower())(endpoint)
    response_data: dict[str, Any] = response.json()

    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED

    assert is_datetime(response_data.pop('timestamp'))

    assert response_data == {
        'name': 'MethodNotAllowed',
        'scope': 'ApiGeneralException',
        'message': f'The {method} method isn\'t allowed for the endpoint {endpoint}',
        'type': 'MethodNotAllowed',
        'status': HTTPStatus.METHOD_NOT_ALLOWED,
    }
