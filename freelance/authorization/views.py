from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests


# классовое представление для подтверждение почты
class ActivateAccountView(APIView):
    permission_classes = [AllowAny]

    # TODO сделать url перменной окружения
    def get(self, request, uid, token):
        url = 'http://127.0.0.1:8000/api/auth/users/activation/'
        data = {'uid': uid, 'token': token}
        response = requests.post(url, data=data)
        if response.ok:
            return Response({'message': 'Аккаунт успешно активирован'})
        else:
            return Response({'message': 'Ошибка при активации аккаунта'}, status=response.status_code)
