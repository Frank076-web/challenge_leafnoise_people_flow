from flask import Request


def pagination_validation(request: Request):
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=50, type=int)

    return page, limit
