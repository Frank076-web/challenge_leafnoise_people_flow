# routes/position_routes.py
from flasgger import swag_from
from flask import Blueprint, request

from use_cases.position import (
    find_positions_use_case,
    create_position_use_case,
    update_position_use_case,
    delete_position_use_case,
    find_position_by_id_use_case,
)

PREFIX = "/positions"

position_bp = Blueprint("positions", __name__)


@position_bp.route(PREFIX, methods=["GET"])
@swag_from("../docs/positions/find_positions.yml")
def find_positions():
    return find_positions_use_case()


@position_bp.route(f"{PREFIX}/<id>", methods=["GET"])
@swag_from("../docs/positions/find_position_by_id.yml")
def find_position_by_id(id):
    return find_position_by_id_use_case(id)


@position_bp.route(PREFIX, methods=["POST"])
@swag_from("../docs/positions/create_position.yml")
def create_position():
    return create_position_use_case(request)


@position_bp.route(f"{PREFIX}/<id>", methods=["PATCH"])
@swag_from("../docs/positions/update_position.yml")
def update_position(id):
    return update_position_use_case(id, request)


@position_bp.route(f"{PREFIX}/<id>", methods=["DELETE"])
@swag_from("../docs/positions/delete_position.yml")
def delete_position(id):
    return delete_position_use_case(id)
