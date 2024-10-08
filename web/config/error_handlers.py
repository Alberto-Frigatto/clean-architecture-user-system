from http import HTTPStatus
from typing import Any

from fastapi import FastAPI, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from usecases.exceptions import AuthException, UserException
from web.exceptions.api import ApiSecurityException, ApiValidationException
from web.exceptions.http import (
    BadRequest,
    Conflict,
    Forbidden,
    Unauthorized,
    UnprocessableEntity,
)
from web.exceptions.http.base import HttpError


def add_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(HttpError)
    def http_error_handler(_: Request, e: HttpError) -> Response:
        return JSONResponse(
            content=jsonable_encoder(e.json()),
            status_code=e.status,
            headers=e.headers,
        )

    # usecase exceptions

    @app.exception_handler(UserException.UserAlreadyExists)
    def user_already_exists_handler(
        _: Request, e: UserException.UserAlreadyExists
    ) -> None:
        raise Conflict(
            name=e.name,
            scope=e.scope,
            message=e.message,
        )

    @app.exception_handler(AuthException.InvalidCredentials)
    def invalid_credentials_handler(
        _: Request, e: AuthException.InvalidCredentials
    ) -> None:
        raise Unauthorized(
            name=e.name,
            scope=e.scope,
            message=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        )

    @app.exception_handler(UserException.UserNotFound)
    def user_not_found_handler(_: Request, e: UserException.UserNotFound) -> None:
        raise Unauthorized(
            name=e.name,
            scope=e.scope,
            message=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        )

    @app.exception_handler(UserException.UserIsUnderage)
    def user_is_under_age_handler(_: Request, e: UserException.UserIsUnderage) -> None:
        raise UnprocessableEntity(
            name=e.name,
            scope=e.scope,
            message=e.message,
        )

    @app.exception_handler(UserException.UserIsDeactivated)
    def user_is_deactivated_handler(
        _: Request, e: UserException.UserIsDeactivated
    ) -> None:
        raise Forbidden(
            name=e.name,
            scope=e.scope,
            message=e.message,
        )

    @app.exception_handler(UserException.OldPasswordDoesntMatch)
    def old_password_doesnt_match_handler(
        _: Request, e: UserException.OldPasswordDoesntMatch
    ) -> None:
        raise Forbidden(
            name=e.name,
            scope=e.scope,
            message=e.message,
        )

    @app.exception_handler(UserException.NewPasswordConfirmationMismatch)
    def new_password_confirmation_mismatch_handler(
        _: Request, e: UserException.NewPasswordConfirmationMismatch
    ) -> None:
        raise BadRequest(
            name=e.name,
            scope=e.scope,
            message=e.message,
        )

    @app.exception_handler(UserException.NewPasswordCantBeSameAsOld)
    def new_password_cant_be_same_as_old_handler(
        _: Request, e: UserException.NewPasswordCantBeSameAsOld
    ) -> None:
        raise BadRequest(
            name=e.name,
            scope=e.scope,
            message=e.message,
        )

    # api errors

    @app.exception_handler(ApiSecurityException.InvalidJwt)
    def invalid_jwt_handler(_: Request, e: ApiSecurityException.InvalidJwt) -> None:
        raise Unauthorized(
            name=e.name,
            scope=e.scope,
            message=e.message,
            detail=e.detail,
            headers={"WWW-Authenticate": "Bearer"},
        )

    @app.exception_handler(ApiSecurityException.ExpiredJwt)
    def expired_jwt_handler(_: Request, e: ApiSecurityException.ExpiredJwt) -> None:
        raise Unauthorized(
            name=e.name,
            scope=e.scope,
            message=e.message,
            detail=e.detail,
            headers={"WWW-Authenticate": "Bearer"},
        )

    # override fastapi error handlers

    @app.exception_handler(RequestValidationError)
    def request_validation_error_handler(_: Request, e: RequestValidationError) -> None:
        def handle_error_item(error: dict[str, Any]) -> dict[str, Any]:
            error['message'] = error.pop('msg')
            error.pop('ctx', None)

            return error

        error: ApiValidationException.InvalidDataSent = (
            ApiValidationException.InvalidDataSent(
                detail=[handle_error_item(error) for error in e.errors()]
            )
        )

        raise BadRequest(
            name=error.name,
            scope=error.scope,
            message=error.message,
            detail=error.detail,
        )

    @app.exception_handler(HTTPStatus.UNAUTHORIZED)
    def missing_jwt_error_handler(*_: Any) -> None:
        error: ApiSecurityException.MissingJwt = ApiSecurityException.MissingJwt()

        raise Unauthorized(
            name=error.name,
            scope=error.scope,
            message=error.message,
            detail=error.detail,
            headers={"WWW-Authenticate": "Bearer"},
        )
