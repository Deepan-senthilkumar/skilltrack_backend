from rest_framework.response import Response
from rest_framework import status


def send_success(message: str, data: any = None, status_code: int = status.HTTP_200_OK) -> Response:
    """
    Standard success response formatter mirroring Backend-setup structure.
    """
    return Response({
        "success": True,
        "message": message,
        "data": data
    }, status=status_code)


def send_error(message: str, status_code: int = status.HTTP_400_BAD_REQUEST, errors: any = None) -> Response:
    """
    Standard error response formatter mirroring Backend-setup structure.
    """
    return Response({
        "success": False,
        "message": message,
        "errors": errors
    }, status=status_code)
