from rest_framework.views import exception_handler

from .response import ApiResponse


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return ApiResponse.error(
            message="Internal server error.",
            status_code=500,
        )

    return ApiResponse.error(
        message="Request failed.",
        errors=response.data,
        status_code=response.status_code,
    )