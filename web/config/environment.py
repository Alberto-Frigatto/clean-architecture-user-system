import os


def is_app_in_production_mode() -> bool:
    environment: str = os.getenv('ENV', 'test').lower()
    accepted_values: tuple[str, str] = (
        'test',
        'production',
    )

    if environment not in accepted_values:
        raise ValueError(
            f'Valor inválido para a variável ENV. Ela deve ser: {", ".join(accepted_values)}'
        )

    return environment == 'production'
