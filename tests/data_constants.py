from typing import Final # Set constants with type annotations

OK_CODE: Final[int] = 200
CREATED_CODE: Final[int] = 201
BAD_REQUEST: Final[int] = 400
INTERNAL_SERVER_ERROR: Final[int] = 500

INVALID_FIRST_NAME_ERROR: Final[str] = 'Has introducido un nombre de usuario no válido. El nombre solo puede contener letras del alfabeto latino, la longitud debe ser de 2 a 15 caracteres.'
MISSING_PARAM_ERROR: Final[str] = 'No se han aprobado todos los parámetros requeridos'
