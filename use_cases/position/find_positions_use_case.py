from models.position import Position
from dtos.position_dto import PositionDto
from config.api_response import ApiResponse


def find_positions_use_case():
    positions = Position.objects(deleted=False)  # type: ignore

    return ApiResponse(
        success=True,
        data=[
            PositionDto(
                id=str(p.id), name=p.name, deleted=p.deleted, deleted_at=p.deleted_at
            )
            for p in positions
        ],
    ).model_dump()
