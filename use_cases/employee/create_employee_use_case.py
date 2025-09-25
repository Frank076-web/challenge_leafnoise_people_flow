from flask import Request
from pydantic import ValidationError

from models.employee import Employee
from models.position import Position
from dtos.position_dto import PositionDto
from config.api_response import ApiResponse
from dtos.employee_dto import EmployeeCreate, EmployeeDto
from shared.mongo_id_validation import mongo_id_validation


def create_employee_use_case(request: Request):
    try:
        employee_data = EmployeeCreate.model_validate(request.get_json()).sanitize()

        employee_duplicate = Employee.objects(email=employee_data.email).first()  # type: ignore

        if employee_duplicate:
            return (
                ApiResponse(
                    success=False, message="Employee with this email already exists"
                ).model_dump(),
                400,
            )

        is_valid, _ = mongo_id_validation(employee_data.position)

        if not is_valid:
            return (
                ApiResponse(
                    success=False, message="The position id is not a valid Mongo ID"
                ).model_dump(),
                400,
            )

        position = Position.objects(id=employee_data.position)  # type: ignore

        if not position:
            return (
                ApiResponse(
                    success=False,
                    message=f"Position with id : {employee_data.position} not found",
                ).model_dump(),
                400,
            )

        new_employee = Employee(**employee_data.model_dump()).save()

        employee = list(Employee.objects(id=new_employee.id).select_related())  # type: ignore
        employee = employee[0]

        return ApiResponse(
            success=True,
            data=EmployeeDto(
                id=str(employee.id),
                name=employee.name,
                last_name=employee.last_name,
                email=employee.email,
                position=PositionDto(
                    id=str(employee.position.id),
                    name=employee.position.name,
                    deleted=employee.position.deleted,
                    deleted_at=employee.position.deleted_at,
                ),
                salary=employee.salary,
                admission_date=employee.admission_date,
                deleted=employee.deleted,
                deleted_at=employee.deleted_at,
            ),
        ).model_dump()

    except ValidationError as e:
        return ApiResponse(success=False, message=str(e.errors())).model_dump(), 400
