from datetime import datetime, timezone

from models.employee import Employee
from config.api_response import ApiResponse
from shared.mongo_id_validation import mongo_id_validation


def delete_employee_use_case(employee_id: str):
    try:
        is_valid, error_msg = mongo_id_validation(employee_id)

        if not is_valid:
            return ApiResponse(success=False, message=error_msg).model_dump(), 400

        employee = Employee.objects(id=employee_id).first()  # type: ignore

        if not employee:
            return (
                ApiResponse(
                    success=False, message=f"Employee with id: {employee_id} not found"
                ).model_dump(),
                404,
            )

        if employee.deleted:
            return (
                ApiResponse(
                    success=False, message=f"Employee with id: {employee_id} not found"
                ).model_dump(),
                404,
            )

        Employee.objects(id=employee_id).update(  # type: ignore
            set__deleted=True, set__deleted_at=datetime.now(timezone.utc)
        )

        return ApiResponse(
            success=True, message=f"Employee with id: {employee_id} deleted"
        ).model_dump()

    except Exception as e:
        return ApiResponse(success=False, message=str(e)).model_dump(), 500
