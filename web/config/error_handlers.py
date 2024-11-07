from http import HTTPStatus
from typing import Any

from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from pydantic_core import ValidationError

from usecases.exceptions import AuthException, UserException
from web.exceptions import (
    ApiGeneralException,
    ApiSecurityException,
    ApiValidationException,
)
from web.http_error_responses import (
    BadRequest,
    Conflict,
    Forbidden,
    MethodNotAllowed,
    NotFound,
    Unauthorized,
    UnprocessableEntity,
)


def add_error_handlers(app: FastAPI) -> None:
    # usecase exceptions

    @app.exception_handler(UserException.UserAlreadyExists)
    def user_already_exists_handler(
        _: Request, e: UserException.UserAlreadyExists
    ) -> Response:
        return Conflict(e).json()

    @app.exception_handler(AuthException.InvalidCredentials)
    def invalid_credentials_handler(
        _: Request, e: AuthException.InvalidCredentials
    ) -> Response:
        return Unauthorized(e, headers={"WWW-Authenticate": "Bearer"}).json()

    @app.exception_handler(UserException.UserNotFound)
    def user_not_found_handler(_: Request, e: UserException.UserNotFound) -> Response:
        return Unauthorized(e, headers={"WWW-Authenticate": "Bearer"}).json()

    @app.exception_handler(UserException.UserIsUnderage)
    def user_is_under_age_handler(
        _: Request, e: UserException.UserIsUnderage
    ) -> Response:
        return UnprocessableEntity(e).json()

    @app.exception_handler(UserException.UserIsDeactivated)
    def user_is_deactivated_handler(
        _: Request, e: UserException.UserIsDeactivated
    ) -> Response:
        return Forbidden(e).json()

    @app.exception_handler(UserException.OldPasswordDoesntMatch)
    def old_password_doesnt_match_handler(
        _: Request, e: UserException.OldPasswordDoesntMatch
    ) -> Response:
        return Forbidden(e).json()

    @app.exception_handler(UserException.NewPasswordConfirmationMismatch)
    def new_password_confirmation_mismatch_handler(
        _: Request, e: UserException.NewPasswordConfirmationMismatch
    ) -> Response:
        return BadRequest(e).json()

    @app.exception_handler(UserException.NewPasswordCantBeSameAsOld)
    def new_password_cant_be_same_as_old_handler(
        _: Request, e: UserException.NewPasswordCantBeSameAsOld
    ) -> Response:
        return BadRequest(e).json()

    # api errors

    @app.exception_handler(ApiSecurityException.InvalidJwt)
    def invalid_jwt_handler(_: Request, e: ApiSecurityException.InvalidJwt) -> Response:
        return Unauthorized(e, headers={"WWW-Authenticate": "Bearer"}).json()

    @app.exception_handler(ApiSecurityException.ExpiredJwt)
    def expired_jwt_handler(_: Request, e: ApiSecurityException.ExpiredJwt) -> Response:
        return Unauthorized(e, headers={"WWW-Authenticate": "Bearer"}).json()

    # override fastapi error handlers

    @app.exception_handler(RequestValidationError)
    def request_validation_error_handler(
        _: Request, e: RequestValidationError
    ) -> Response:
        def handle_error_item(error: dict[str, Any]) -> dict[str, Any]:
            error['message'] = error.pop('msg')
            error.pop('ctx', None)

            return error

        return BadRequest(
            ApiValidationException.InvalidDataSent(
                detail=[handle_error_item(error) for error in e.errors()]
            )
        ).json()

    @app.exception_handler(ValidationError)
    def validation_error_handler(_: Request, e: ValidationError) -> Response:
        def handle_error_item(error: dict[str, Any]) -> dict[str, Any]:
            error['message'] = error.pop('msg')
            error['loc'] = 'body', error['loc'][0]

            return error

        return BadRequest(
            ApiValidationException.InvalidDataSent(
                detail=[
                    handle_error_item(dict(error))
                    for error in e.errors(include_context=False, include_url=False)
                ]
            )
        ).json()

    @app.exception_handler(HTTPStatus.UNAUTHORIZED)
    def missing_jwt_error_handler(*_: Any) -> Response:
        return Unauthorized(
            ApiSecurityException.MissingJwt(), headers={"WWW-Authenticate": "Bearer"}
        ).json()

    @app.exception_handler(HTTPStatus.NOT_FOUND)
    def endpoint_not_found_error_handler(request: Request, _: Exception) -> Response:
        return NotFound(ApiGeneralException.EndpointNotFound(request.url.path)).json()

    @app.exception_handler(HTTPStatus.METHOD_NOT_ALLOWED)
    def method_not_allowed_error_handler(request: Request, _: Exception) -> Response:
        return MethodNotAllowed(
            ApiGeneralException.MethodNotAllowed(
                method=request.method, endpoint=request.url.path
            )
        ).json()
