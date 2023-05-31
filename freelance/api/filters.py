from django_filters import rest_framework as filters
from api.models import Task


class TaskFilter(filters.FilterSet):
    """
    Фильтрует строку поиска по категориям и названию модели Task
    """

    category_id = filters.CharFilter(field_name="category__id")

    title = filters.CharFilter(field_name="title", lookup_expr="icontains")

    class Meta:
        model = Task
        fields = ("title", "category_id")
