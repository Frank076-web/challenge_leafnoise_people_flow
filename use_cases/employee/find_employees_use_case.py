from math import ceil
from typing import Any
from bson import ObjectId
from flask import Request

from dtos.position_dto import PositionDto
from models.employee import Employee
from config.api_response import ApiResponse
from dtos.employee_dto import EmployeeDto, EmployeeFindAll
from shared.pagination_validation import pagination_validation


def find_employees_use_case(request: Request):
    position = request.args.get("position", type=str)
    page, limit = pagination_validation(request)

    filters: dict[str, Any] = {"deleted": False}

    if position:
        filters["position"] = ObjectId(position)

    offset = (page - 1) * limit
    employees = Employee.objects(**filters).skip(offset).limit(limit).select_related()  # type: ignore

    total = Employee.objects(**filters).count()  # type: ignore
    pages = ceil(total / limit)

    return ApiResponse(
        success=True,
        data=EmployeeFindAll(
            total=total,
            pages=pages,
            employees=[
                EmployeeDto(
                    id=str(e.id),
                    name=e.name,
                    last_name=e.last_name,
                    email=e.email,
                    position=PositionDto(
                        id=str(e.position.id),
                        name=e.position.name,
                        deleted=e.position.deleted,
                        deleted_at=e.position.deleted_at,
                    ),
                    salary=e.salary,
                    admission_date=e.admission_date,
                    deleted=e.deleted,
                    deleted_at=e.deleted_at,
                )
                for e in employees
            ],
        ),
    ).model_dump()
