from flask import Request
from pydantic import ValidationError

from models.employee import Employee
from models.position import Position
from dtos.position_dto import PositionDto
from config.api_response import ApiResponse
from dtos.employee_dto import EmployeeUpdate, EmployeeDto
from shared.mongo_id_validation import mongo_id_validation


def update_employee_use_case(employee_id: str, request: Request):
    try:
        # Validate Employee ID
        is_valid, error_msg = mongo_id_validation(employee_id)
        if not is_valid:
            return ApiResponse(success=False, message=error_msg).model_dump(), 400

        # Get current employee
        actual_employee = Employee.objects(id=employee_id).first()  # type: ignore
        if not actual_employee:
            return (
                ApiResponse(
                    success=False, message=f"Employee with id: {employee_id} not found"
                ).model_dump(),
                400,
            )

        # Get submitted data
        entry_data = request.get_json() or {}
        employee_data = EmployeeUpdate.model_validate(entry_data).sanitize()

        if not any(employee_data.model_dump(exclude_unset=True).values()):
            return (
                ApiResponse(success=False, message="No fields to update").model_dump(),
                400,
            )

        # Validate duplicate email
        if employee_data.email:
            employee_duplicate = Employee.objects(email=employee_data.email).first()  # type: ignore
            if employee_duplicate and str(employee_duplicate.id) != employee_id:
                return (
                    ApiResponse(
                        success=False, message="Employee with this email already exists"
                    ).model_dump(),
                    400,
                )

        # Validate and assign position if applicable
        if employee_data.position:
            position_doc = Position.objects(id=employee_data.position).first()  # type: ignore
            if not position_doc:
                return (
                    ApiResponse(
                        success=False,
                        message=f"Position with id {employee_data.position} not found",
                    ).model_dump(),
                    400,
                )

            # Replace id with document
            employee_data.position = position_doc

        # Update employee in DB
        update_dict = {
            f"set__{k}": v
            for k, v in employee_data.model_dump(exclude_unset=True).items()
            if v is not None
        }
        Employee.objects(id=employee_id).update(**update_dict)  # type: ignore

        # Get updated employee
        employee = list(Employee.objects(id=employee_id).select_related())[0]  # type: ignore

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

    except Exception as e:
        return ApiResponse(success=False, message=str(e)).model_dump(), 500
