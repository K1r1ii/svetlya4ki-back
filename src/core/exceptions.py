class DatabaseError(Exception):
    """ Ошибка при работе с базой данных (вина пользователя) """
    ...


class DatabaseInternalError(Exception):
    """ Ошибка при работе с базой данных (внутренняя ошибка) """