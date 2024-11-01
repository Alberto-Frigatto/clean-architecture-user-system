from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from adapters.id import UlidManager
from adapters.repositories.user import MongoUserRepository
from adapters.security import BcryptPasswordManager
from ports.id import IIdManager
from ports.repositories.user import IUserRepository
from ports.security import IPasswordManager
from usecases.auth import AuthenticateUserUsecase
from usecases.user import (
    CreateUserUsecase,
    DeactivateUserUsecase,
    GetActiveUserUsecase,
    UpdateUserPasswordUsecase,
    UpdateUserPersonalDataUsecase,
    UpdateUserPreferencesUsecase,
)
from web.config.settings import ProdSettings, TestSettings
from web.config.settings.base import Settings
from web.db import MongoConnection
from web.di import Di
from web.security import IJwtManager
from web.security.impl import PyJwtManager


def config_di(*, test: bool) -> None:
    Di.map(
        IJwtManager,
        to=PyJwtManager,
        singleton=True,
    )

    # db connection
    Di.map(
        AsyncIOMotorClient,
        to=MongoConnection.get_client,
        singleton=True,
    )
    Di.map(
        AsyncIOMotorDatabase,
        to=MongoConnection.get_db,
        singleton=True,
    )

    # objects
    if test:
        Di.map(
            Settings,
            to=TestSettings(),  # type: ignore
            singleton=True,
        )
    else:
        Di.map(
            Settings,
            to=ProdSettings(),  # type: ignore
            singleton=True,
        )

    # ports adapters
    Di.map(
        IUserRepository,
        to=MongoUserRepository,
        singleton=True,
    )
    Di.map(
        IPasswordManager,
        to=BcryptPasswordManager,
        singleton=True,
    )
    Di.map(
        IIdManager,
        to=UlidManager,
        singleton=True,
    )

    # usecases
    Di.map(
        AuthenticateUserUsecase,
        to=AuthenticateUserUsecase,
        singleton=True,
    )
    Di.map(
        CreateUserUsecase,
        to=CreateUserUsecase,
        singleton=True,
    )
    Di.map(
        DeactivateUserUsecase,
        to=DeactivateUserUsecase,
        singleton=True,
    )
    Di.map(
        GetActiveUserUsecase,
        to=GetActiveUserUsecase,
        singleton=True,
    )
    Di.map(
        UpdateUserPasswordUsecase,
        to=UpdateUserPasswordUsecase,
        singleton=True,
    )
    Di.map(
        UpdateUserPersonalDataUsecase,
        to=UpdateUserPersonalDataUsecase,
        singleton=True,
    )
    Di.map(
        UpdateUserPreferencesUsecase,
        to=UpdateUserPreferencesUsecase,
        singleton=True,
    )
