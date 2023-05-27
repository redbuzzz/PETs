import http

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import GenericViewSet

from .filters import TaskFilter
from .serializers import TaskSerializer, BidSerializer, UserSerializer, CategorySerializer, ProfileGetSerializer, \
    ProfilePostSerializer, ProfilePutSerializer
from .models import Task, Bid, Category, Profile


class TaskViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskFilter
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = []


class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            pass
        elif self.request.method == 'POST':
            return BidSerializer

    def create(self, request, *args, **kwargs):
        task_id = kwargs.get('task_id')
        serializer = BidSerializer(data=request.data, context={'user': request.user, 'task_id': task_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# для проверки аутентификации
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class CategoryViewSet(mixins.ListModelMixin, GenericViewSet):
    pagination_class = None
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProfileViewSet(APIView):

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProfileGetSerializer
        elif self.request.method in ['PUT', 'PATCH']:
            return ProfilePutSerializer
        elif self.request.method == 'POST':
            return ProfilePostSerializer

    def get_profile(self):
        return Profile.objects.get(user=self.request.user)

    def get(self, request, *args, **kwargs):
        profile = self.get_profile()
        serializer = ProfileGetSerializer(profile)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        profile = self.get_profile()
        serializer = serializer_class(instance=profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        profile = self.get_profile()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# todo для смены почты использовать встроенный сериализатор в djoser

class ProfileCheck(APIView):
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProfileGetSerializer

    def get_profile(self):
        try:
            return Profile.objects.get(user=self.request.user)
        except ObjectDoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        profile = self.get_profile()
        if profile is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_200_OK)
