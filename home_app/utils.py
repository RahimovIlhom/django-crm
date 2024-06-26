from django.http import Http404
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None and isinstance(exc, Http404):
        response = Response({'success': False, 'message': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
    elif response is not None:
        response.data['status_code'] = response.status_code

    return response
