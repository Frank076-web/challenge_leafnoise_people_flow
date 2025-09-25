from flasgger import swag_from
from flask import Blueprint, request
from use_cases.employee import (
    find_employees_use_case,
    create_employee_use_case,
    update_employee_use_case,
    delete_employee_use_case,
    find_employee_by_id_use_case,
    get_calculated_salary_average_use_case,
)

PREFIX = "/employees"

employees_bp = Blueprint("employees", __name__)


@swag_from("../docs/employees/find_employees.yml")
@employees_bp.route(PREFIX, methods=["GET"])
def find_employees():
    return find_employees_use_case(request)


@swag_from("../docs/employees/find_employee_by_id.yml")
@employees_bp.route(f"{PREFIX}/<id>", methods=["GET"])
def find_employee_by_id(id):
    return find_employee_by_id_use_case(id)


@swag_from("../docs/employees/create_employee.yml")
@employees_bp.route(PREFIX, methods=["POST"])
def create_employee():
    return create_employee_use_case(request)


@swag_from("../docs/employees/update_employee.yml")
@employees_bp.route(f"{PREFIX}/<id>", methods=["PATCH"])
def update_employee(id):
    return update_employee_use_case(id, request)


@swag_from("../docs/employees/delete_employee.yml")
@employees_bp.route(f"{PREFIX}/<id>", methods=["DELETE"])
def delete_employee(id):  # -> Any:
    return delete_employee_use_case(id)


@swag_from("../docs/employees/salary_average.yml")
@employees_bp.route(f"{PREFIX}/salary_average", methods=["GET"])
def get_calculated_salary_average():  # -> Any:
    return get_calculated_salary_average_use_case()
