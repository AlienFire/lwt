from enum import StrEnum


class ContentStatusEnum(StrEnum):
    finished = "Просмотрено"
    is_active = "В процессе просмотра"
    at_plan = "В плане на просмотр"
    dropped = "Брошено"
