import secrets

import pytest
from fastapi import FastAPI

from web.app import create_app
from web.config.settings import ProdSettings, TestSettings
from web.config.settings.base import Settings
from web.di import Di
from web.main import app


def test_when_ENV_env_var_is_production_the_app_is_created_in_production_mode(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv('ENV', 'production')
    monkeypatch.setenv('SECRET_KEY', secrets.token_hex())

    app: FastAPI = create_app()

    assert 'produção' in app.title.lower()

    settings: Settings = Di.get_raw(Settings)

    assert isinstance(settings, ProdSettings)


def test_when_ENV_env_var_is_test_the_app_is_created_in_test_mode(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv('ENV', 'test')
    monkeypatch.setenv('SECRET_KEY', secrets.token_hex())

    app: FastAPI = create_app()

    assert 'teste' in app.title.lower()

    settings: Settings = Di.get_raw(Settings)

    assert isinstance(settings, TestSettings)


def test_when_provide_an_invalid_value_for_ENV_env_var_raises_ValueError(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv('ENV', 'abc')

    with pytest.raises(ValueError):
        create_app()


def test_app_instance_in_main_py_is_FastAPI() -> None:
    assert isinstance(app, FastAPI)
