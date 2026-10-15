import logging
from django.http import JsonResponse
from rest_framework import status

logger = logging.getLogger(__name__)


class APIErrorHandlingMiddleware:
    """
    Catches unhandled server exceptions and returns standardized JSON response
    matching the Backend-setup error handler format.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        logger.exception("Unhandled Exception occurred during request to %s", request.path)
        
        # Only handle API requests
        if request.path.startswith('/api/'):
            return JsonResponse({
                "success": False,
                "message": str(exception),
                "errors": None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return None
