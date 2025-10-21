SUCCESS = {
    200: {
        "description": "OK",
        "content": {"application/json": {"example": {"detail": "Успешный запрос."}}},
    }
}

BAD_REQUEST = {
    400: {
        "description": "Bad Request",
        "content": {
            "application/json": {
                "example": {"detail": "Обнаружена ошибка в запросе."}
            }
        },
    }
}

UNAUTHORIZED = {
    401: {
        "description": "Unauthorized",
        "content": {
            "application/json": {"example": {"detail": "Ошибка авторизации."}}
        },
    }
}

FORBIDDEN = {
    403: {
        "description": "Forbidden",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Сервер принял запрос, но доступ к ресурсу запрещен."
                }
            }
        },
    }
}

NOT_FOUND = {
    404: {
        "description": "Not Found",
        "content": {
            "application/json": {
                "example": {"detail": "Ресурс не найден."}
            }
        },
    }
}

CONFLICT = {
    409: {
        "description": "Conflict",
        "content": {
            "application/json": {"example": {"detail": "Возникла конфликтная ситуация при доступе к ресурсу."}}
        },
    }
}


UNPROCESSABLE_ENTITY = {
    422: {
        "description": "Unprocessable Entity",
        "content": {
            "application/json": {"example": {"detail": "Ошибка валидации данных"}}
        },
    }
}
