from models.employee import Employee
from config.api_response import ApiResponse


def get_calculated_salary_average_use_case():
    result = Employee.objects.aggregate(  # type: ignore
        {"$match": {"deleted": False}},
        {"$group": {"_id": None, "average_salary": {"$avg": "$salary"}}},
    )
    result = list(result)

    return ApiResponse(
        success=True,
        data={"average_salary": round(result[0]["average_salary"], 2) if result else 0},
    ).model_dump()
