from enum import Enum

token = '2044678461:AAHed6zJlMxBCWUjUCtBp5XyzHMtMZ9Jyf0'
db_file = "database.vdb"


class States(Enum):
    """
    Мы используем БД Vedis, в которой хранимые значения всегда строки,
    поэтому и тут будем использовать тоже строки (str)
    """
    S_START = "0"  # Начало нового диалога
    S_ENTER_SOURCE = "1" # Указать источник
    S_ENTER_LIMITING_NUM = "2" # Указать кол-во новостей