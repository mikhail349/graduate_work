from django.http import JsonResponse
from rest_framework.decorators import api_view

from auth.decorators import user_required


@api_view(['GET'])
@user_required
def get_subscriptions(request, user):
    print(user)
    return JsonResponse('Ok', safe=False)
