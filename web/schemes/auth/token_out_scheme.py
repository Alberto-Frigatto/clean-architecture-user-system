from web.schemes.base import OutScheme


class TokenOutScheme(OutScheme):
    access_token: str
    token_type: str = 'bearer'
