from flask import Request
from models.position import Position
from config.api_response import ApiResponse
from dtos.position_dto import PositionDto, PositionUpdate
from shared.mongo_id_validation import mongo_id_validation


def update_position_use_case(position_id: str, request: Request):
    is_valid, error_msg = mongo_id_validation(position_id)
    if not is_valid:
        return ApiResponse(success=False, message=error_msg).model_dump(), 400

    data = PositionUpdate.model_validate(request.get_json()).sanitize()

    update_data = {
        f"set__{k}": v
        for k, v in data.model_dump(exclude_unset=True).items()
        if v is not None
    }

    if not update_data:
        return (
            ApiResponse(success=False, message="No fields to update").model_dump(),
            400,
        )

    Position.objects(id=position_id).update(**update_data)  # type: ignore

    updated = Position.objects(id=position_id).first()  # type: ignore

    return ApiResponse(
        success=True,
        data=PositionDto(
            id=str(updated.id),
            name=updated.name,
            deleted=updated.deleted,
            deleted_at=updated.deleted_at,
        ),
    ).model_dump()
