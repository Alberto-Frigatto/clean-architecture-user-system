from typing import Any

CreateUserScheme_example: dict[str, Any] = {
    'username': 'Marcos Rocha Figueiredo',
    'email': 'marcos.figueiredo@hotmail.com.br',
    'password': 'ye5s(D!S',
    'birth_date': '1993-04-17',
    'color_theme': 'dark',
    'language': 'pt_br',
}

UpdateUserPasswordScheme_example: dict[str, Any] = {
    'old_password': 'ye5s(D!S',
    'new_password': 'TE94U@2T',
    'confirm_new_password': 'TE94U@2T',
}

UpdateUserPersonalDataScheme_example: dict[str, Any] = {
    'username': 'Marcos Rocha Figueiredo',
    'email': 'marcos.figueiredo@hotmail.com.br',
    'birth_date': '1993-04-17',
}

UpdateUserPreferencesScheme_example: dict[str, Any] = {
    'color_theme': 'dark',
    'language': 'pt_br',
}

UserOutScheme_example: dict[str, Any] = {
    'id': '01JB8GT124Y8GJ8FDQGWR91X3J',
    'username': 'Marcos Rocha Figueiredo',
    'email': 'marcos.figueiredo@hotmail.com.br',
    'password': 'ye5s(D!S',
    'birth_date': '1993-04-17',
    'color_theme': 'dark',
    'language': 'pt_br',
    'is_active': True,
    'created_at': '2024-10-28T02:54:27.746Z',
}
