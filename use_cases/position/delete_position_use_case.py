from models.position import Position
from datetime import datetime, timezone
from config.api_response import ApiResponse
from shared.mongo_id_validation import mongo_id_validation


def delete_position_use_case(position_id: str):
    is_valid, error_msg = mongo_id_validation(position_id)
    if not is_valid:
        return ApiResponse(success=False, message=error_msg).model_dump(), 400

    position = Position.objects(id=position_id).first()  # type: ignore

    if not position:
        return (
            ApiResponse(
                success=False, message=f"Position with id: {position_id} not found"
            ).model_dump(),
            404,
        )

    if position["deleted"]:
        return (
            ApiResponse(
                success=False, message=f"Position with id: {position_id} not found"
            ).model_dump(),
            404,
        )

    Position.objects(id=position_id).update(  # type: ignore
        set__deleted=True, set__deleted_at=datetime.now(timezone.utc)
    )

    return ApiResponse(
        success=True, message=f"Position with id: {position_id} deleted"
    ).model_dump()
