authenticate_user_description: str = """
Autentica um usuário e gera um token de acesso **JWT**.

Este endpoint recebe as credenciais de um usuário e autentica-o.

Em caso de sucesso, retorna um token JWT, que pode ser utilizado para autorizar outras requisições à API.

- **Request Body**: credenciais do usuário.
    - **username** (string) - E-mail do usuário
    - **password** (string) - Senha do usuário

- **Response**: token JWT.
    - **access_token** (string) - Token JWT
    - **token_type** (string) - Tipo de token JWT, fixo como `bearer`
"""
