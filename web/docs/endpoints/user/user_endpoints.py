create_user_description: str = '''
Cria um novo usuário no sistema.

Este endpoint recebe os dados de um usuário e o registra no sistema, retornando os dados do usuário criado.

- **Request Body**: informações do usuário.
    - **birth_date** (string, formato: YYYY-MM-DD) - Data de nascimento do usuário.
    - **color_theme** (string) - Tema de cor preferido do usuário.
    - **email** (string) - E-mail do usuário.
    - **language** (string) - Idioma preferido do usuário.
    - **password** (string) - Senha do usuário.
    - **username** (string) - Nome completo do usuário.

- **Response**: dados do usuário criado.
    - **birth_date** (string, formato: YYYY-MM-DD) - Data de nascimento do usuário.
    - **color_theme** (string) - Tema de cor preferido do usuário.
    - **created_at** (string, formato: ISO 8601) - Data e hora em que o usuário foi criado.
    - **email** (string) - E-mail do usuário.
    - **id** (string) - Identificador único do usuário.
    - **is_active** (boolean) - Indica se o usuário está ativo.
    - **language** (string) - Idioma preferido do usuário.
    - **username** (string) - Nome completo do usuário.
'''


get_user_info_description: str = '''
Obtém as informações do usuário autenticado.

Este endpoint retorna os dados do usuário atualmente autenticado, com base no token de autenticação fornecido.

- **Authorization**: Requer um token JWT válido no cabeçalho de autorização.

- **Response**: dados do usuário autenticado.
    - **birth_date** (string, formato: YYYY-MM-DD) - Data de nascimento do usuário.
    - **color_theme** (string) - Tema de cor preferido do usuário.
    - **created_at** (string, formato: ISO 8601) - Data e hora em que o usuário foi criado.
    - **email** (string) - E-mail do usuário.
    - **id** (string) - Identificador único do usuário.
    - **is_active** (boolean) - Indica se o usuário está ativo.
    - **language** (string) - Idioma preferido do usuário.
    - **username** (string) - Nome completo do usuário.
'''

update_user_personal_data_description: str = """
Atualiza os dados pessoais do usuário autenticado.

Este endpoint permite que o usuário autenticado atualize suas informações pessoais.

Em caso de sucesso, retorna os dados atualizados do usuário.

- **Authorization**: Requer um token JWT válido no cabeçalho de autorização.

- **Request Body**: informações pessoais a serem atualizadas.
    - **birth_date** (string, formato: YYYY-MM-DD) - Nova data de nascimento do usuário.
    - **email** (string) - Novo e-mail do usuário.
    - **username** (string) - Novo nome completo do usuário.

- **Response**: dados do usuário atualizado.
    - **birth_date** (string, formato: YYYY-MM-DD) - Data de nascimento do usuário.
    - **color_theme** (string) - Tema de cor preferido do usuário.
    - **created_at** (string, formato: ISO 8601) - Data e hora em que o usuário foi criado.
    - **email** (string) - E-mail do usuário.
    - **id** (string) - Identificador único do usuário.
    - **is_active** (boolean) - Indica se o usuário está ativo.
    - **language** (string) - Idioma preferido do usuário.
    - **username** (string) - Nome completo do usuário.
"""

deactivate_user_description: str = """
Desativa a conta do usuário autenticado.

Este endpoint permite que o usuário autenticado desative sua conta.
Em caso de sucesso, não retorna conteúdo, mas indica que a conta foi desativada.

- **Authorization**: Requer um token JWT válido no cabeçalho de autorização.
"""

update_user_preferences_description: str = """
Atualiza as preferências do usuário autenticado.

Este endpoint permite que o usuário autenticado atualize suas preferências de interface e idioma.

Em caso de sucesso, retorna os dados atualizados do usuário.

- **Authorization**: Requer um token JWT válido no cabeçalho de autorização.

- **Request Body**: preferências a serem atualizadas.
    - **color_theme** (string) - Novo tema de cor preferido do usuário.
    - **language** (string) - Novo idioma preferido do usuário.

- **Response**: dados do usuário atualizado.
    - **birth_date** (string, formato: YYYY-MM-DD) - Data de nascimento do usuário.
    - **color_theme** (string) - Tema de cor preferido do usuário.
    - **created_at** (string, formato: ISO 8601) - Data e hora em que o usuário foi criado.
    - **email** (string) - E-mail do usuário.
    - **id** (string) - Identificador único do usuário.
    - **is_active** (boolean) - Indica se o usuário está ativo.
    - **language** (string) - Idioma preferido do usuário.
    - **username** (string) - Nome completo do usuário.
"""

update_user_password_description: str = """
Atualiza a senha do usuário autenticado.

Este endpoint permite que o usuário autenticado altere sua senha.

Em caso de sucesso, retorna os dados atualizados do usuário.

- **Authorization**: Requer um token JWT válido no cabeçalho de autorização.

- **Request Body**: dados necessários para a atualização da senha.
    - **old_password** (string) - Senha atual do usuário, usada para verificação.
    - **new_password** (string) - Nova senha que o usuário deseja definir.
    - **confirm_new_password** (string) - Confirmação da nova senha; deve ser igual a **new_password**.

- **Response**: dados do usuário atualizado.
    - **birth_date** (string, formato: YYYY-MM-DD) - Data de nascimento do usuário.
    - **color_theme** (string) - Tema de cor preferido do usuário.
    - **created_at** (string, formato: ISO 8601) - Data e hora em que o usuário foi criado.
    - **email** (string) - E-mail do usuário.
    - **id** (string) - Identificador único do usuário.
    - **is_active** (boolean) - Indica se o usuário está ativo.
    - **language** (string) - Idioma preferido do usuário.
    - **username** (string) - Nome completo do usuário.
"""
