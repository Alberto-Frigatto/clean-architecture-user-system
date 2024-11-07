class UserSchemeException:
    class InvalidBirthDate(ValueError):
        def __init__(self) -> None:
            super().__init__('Invalid birth date')

    class PasswordHasNoNecessaryChars(ValueError):
        def __init__(self) -> None:
            super().__init__('Password doesn\'t have the required characters')
