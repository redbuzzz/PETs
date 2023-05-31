from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, BidViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
urlpatterns = [
                  path('tasks/<int:task_id>/bid/', BidViewSet.as_view({'post': 'create'}),
                       name='task-bid-create'),
              ] + router.urls
