from django.http import JsonResponse
from rest_framework.decorators import api_view

from auth.decorators import user_required
from subscriptions.tasks import add_line_to_file

@api_view(['GET'])
@user_required
def get_subscriptions(request, user):
    """тестовый api"""
    add_line_to_file.delay("get_subscriptions")
    return JsonResponse(user, safe=False)
