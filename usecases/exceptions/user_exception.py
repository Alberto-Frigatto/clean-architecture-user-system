from usecases.exceptions.base import AppException


class UserException:
    class UserAlreadyExists(AppException):
        def __init__(self, email: str) -> None:
            super().__init__(message=f'The user {email} already exists')

    class UserNotFound(AppException):
        def __init__(self, user_id: str) -> None:
            super().__init__(message=f'The user {user_id} wasn\'t found')

    class UserIsDeactivated(AppException):
        def __init__(self, email: str) -> None:
            super().__init__(message=f'The user {email} is deactivated')

    class NewPasswordCantBeSameAsOld(AppException):
        def __init__(self, email: str) -> None:
            super().__init__(
                message=f'The user\'s new password {email} can\'t be the same as the old one'
            )

    class NewPasswordConfirmationMismatch(AppException):
        def __init__(self) -> None:
            super().__init__(
                message='New password confirmation doesn\'t match the password provided'
            )

    class OldPasswordDoesntMatch(AppException):
        def __init__(self) -> None:
            super().__init__(
                message='The old password provided does not match the real one'
            )

    class UserIsUnderage(AppException):
        def __init__(self) -> None:
            super().__init__(message='The user is underage')
