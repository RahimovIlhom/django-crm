from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


class NotFoundMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if response.status_code == 404:
            return JsonResponse({'detail': 'Manzil topilmadi.'}, status=404)
        return response
