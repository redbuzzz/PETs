from django.urls import path, re_path
from rest_framework.routers import DefaultRouter

from .views import (
    TaskViewSet,
    BidViewSet,
    ProfileView,
    CategoryViewSet,
    ProfileViewSet,
    ProfileCheck,
    CreateCustomerView,
    CreateFreelancerView,
    SwitchRoleViewSet,
)
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="task")
router.register(r"category", CategoryViewSet, basename="category")
router.register(r"create_customer", CreateCustomerView, basename="create_customer")
router.register(
    r"create_freelancer", CreateFreelancerView, basename="create_freelancer"
)
schema_view = get_schema_view(
    openapi.Info(
        title="Freelance API",
        default_version="v1",
        description="django test project",
        contact=openapi.Contact(email="redbuzzzzzz@gmail.com"),
    ),
    public=True,
    permission_classes=[],
)
urlpatterns = [
    path(
        "tasks/<int:task_id>/bid/",
        BidViewSet.as_view({"post": "create"}),
        name="task-bid-create",
    ),
    path("profile/", ProfileViewSet.as_view(), name="profile"),
    path("profile_check/", ProfileCheck.as_view(), name="profile_check"),
    path("switch_role/", SwitchRoleViewSet.as_view({"patch": "update"})),
    path("is_auth/", ProfileView.as_view()),
    re_path(
        "^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
] + router.urls
