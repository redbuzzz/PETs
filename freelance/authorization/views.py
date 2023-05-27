from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
import requests


# классовое представление для подтверждение почты
class ActivateAccountView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uid, token):
        # todo сделать перменной окружения
        url = 'http://127.0.0.1:8002/api/auth/users/activation/'
        data = {'uid': uid, 'token': token}
        response = requests.post(url, data=data)
        if response.ok:
            return Response({'message': 'Аккаунт успешно активирован'})
        else:
            return Response({'message': 'Ошибка при активации аккаунта'}, status=response.status_code)
