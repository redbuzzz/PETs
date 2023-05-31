from rest_framework import viewsets, status
from rest_framework.response import Response

from .serializers import TaskSerializer, BidSerializer
from .models import Task, Bid


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = []


class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    permission_classes = []

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
