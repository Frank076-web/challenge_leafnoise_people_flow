from models.position import Position
from dtos.position_dto import PositionDto
from config.api_response import ApiResponse
from shared.mongo_id_validation import mongo_id_validation


def find_position_by_id_use_case(position_id: str):
    is_valid, _ = mongo_id_validation(position_id)

    if not is_valid:
        return (
            ApiResponse(
                success=False, message="The position id is not a valid Mongo ID"
            ).model_dump(),
            400,
        )

    position = Position.objects(id=position_id).first()  # type: ignore

    if not position:
        return (
            ApiResponse(
                success=False,
                message=f"Position with id : {position_id} not found",
            ).model_dump(),
            400,
        )

    return ApiResponse(
        success=True,
        data=PositionDto(
            id=str(position.id),
            name=position.name,
            deleted=position.deleted,
            deleted_at=position.deleted_at,
        ),
    ).model_dump()
