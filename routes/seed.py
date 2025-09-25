from flask import Blueprint
from flasgger import swag_from
from datetime import datetime, timezone

from models.position import Position
from models.employee import Employee
from config.api_response import ApiResponse

seed_bp = Blueprint("seed", __name__)


@swag_from("../docs/seed/seed.yml")
@seed_bp.route("/seed", methods=["GET"])
def seed_database():
    try:
        Employee.objects.delete()  # type: ignore
        Position.objects.delete()  # type: ignore

        positions_data = [
            {"name": "manager"},
            {"name": "developer"},
            {"name": "designer"},
            {"name": "qa"},
            {"name": "hr"},
            {"name": "support"},
        ]
        positions = []
        for pos in positions_data:
            position = Position(
                name=pos["name"],
                deleted=False,
                deleted_at=None,
            ).save()
            positions.append(position)

        employees_data = [
            {
                "name": "john",
                "last_name": "doe",
                "email": "john.doe@example.com",
                "position": positions[1],
                "salary": 5000,
                "admission_date": datetime.now(timezone.utc),
                "deleted": False,
                "deleted_at": None,
            },
            {
                "name": "jane",
                "last_name": "smith",
                "email": "jane.smith@example.com",
                "position": positions[0],
                "salary": 8000,
                "admission_date": datetime.now(timezone.utc),
                "deleted": False,
                "deleted_at": None,
            },
            {
                "name": "alice",
                "last_name": "brown",
                "email": "alice.brown@example.com",
                "position": positions[2],
                "salary": 4500,
                "admission_date": datetime.now(timezone.utc),
                "deleted": False,
                "deleted_at": None,
            },
            {
                "name": "bob",
                "last_name": "johnson",
                "email": "bob.johnson@example.com",
                "position": positions[3],
                "salary": 4000,
                "admission_date": datetime.now(timezone.utc),
                "deleted": False,
                "deleted_at": None,
            },
            {
                "name": "charlie",
                "last_name": "davis",
                "email": "charlie.davis@example.com",
                "position": positions[4],
                "salary": 4200,
                "admission_date": datetime.now(timezone.utc),
                "deleted": False,
                "deleted_at": None,
            },
            {
                "name": "eve",
                "last_name": "wilson",
                "email": "eve.wilson@example.com",
                "position": positions[5],
                "salary": 3800,
                "admission_date": datetime.now(timezone.utc),
                "deleted": False,
                "deleted_at": None,
            },
            {
                "name": "frank",
                "last_name": "inzerillo",
                "email": "francoeinzerillo@gmail.com",
                "position": positions[1],
                "salary": 5200,
                "admission_date": datetime.now(timezone.utc),
                "deleted": False,
                "deleted_at": None,
            },
        ]

        for emp in employees_data:
            Employee(**emp).save()

        return ApiResponse(
            success=True,
            message="Database seeded successfully with positions and employees",
        ).model_dump()

    except Exception as e:
        return ApiResponse(success=False, message=str(e)).model_dump(), 500
