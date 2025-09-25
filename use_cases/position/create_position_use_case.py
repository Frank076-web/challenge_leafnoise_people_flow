from flask import Request

from models.position import Position
from config.api_response import ApiResponse
from dtos.position_dto import PositionCreate, PositionDto


def create_position_use_case(request: Request):
    data = PositionCreate.model_validate(request.get_json()).sanitize()

    existing = Position.objects(name=data.name).first()  # type: ignore

    if existing:
        return (
            ApiResponse(success=False, message="Position already exists").model_dump(),
            400,
        )

    new_position = Position(name=data.name).save()

    return ApiResponse(
        success=True,
        data=PositionDto(
            id=str(new_position.id),
            name=new_position.name,
            deleted=new_position.deleted,
            deleted_at=new_position.deleted_at,
        ),
    ).model_dump()
