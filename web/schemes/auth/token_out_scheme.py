from typing import Any

from web.docs.examples.schemes.auth_schemes import TokenOutScheme_example
from web.schemes.base import OutScheme


class TokenOutScheme(OutScheme):
    access_token: str
    token_type: str = 'bearer'

    model_config: dict[str, Any] = {  # type: ignore
        'json_schema_extra': {
            'examples': [TokenOutScheme_example],
        }
    }
