from bson import ObjectId
from typing import Optional


def mongo_id_validation(id: str) -> tuple[bool, Optional[str]]:
    if not ObjectId.is_valid(id):
        return (False, "id must be a valid mongo id")

    return (True, None)
