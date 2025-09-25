from models.employee import Employee
from dtos.position_dto import PositionDto
from dtos.employee_dto import EmployeeDto
from config.api_response import ApiResponse
from shared.mongo_id_validation import mongo_id_validation


def find_employee_by_id_use_case(employee_id: str):
    is_valid, error_msg = mongo_id_validation(employee_id)

    if not is_valid:
        return ApiResponse(success=False, message=error_msg).model_dump(), 400

    employees = list(Employee.objects(id=employee_id).select_related())  # type: ignore

    if len(employees) == 0 or employees[0].deleted:
        return (
            ApiResponse(
                success=False, message=f"Employee with id {employee_id} not found"
            ).model_dump(),
            404,
        )

    employee = employees[0]

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
