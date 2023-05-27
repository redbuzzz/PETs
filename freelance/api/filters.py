from django_filters import rest_framework as filters

from api.models import Task, Category


class TaskFilter(filters.FilterSet):
    category_id = filters.ModelChoiceFilter(queryset=Category.objects.all(), method="filter_category_id")

    def filter_category_id(self, queryset, name, value):
        return queryset.filter(category__in=[value])

    class Meta:
        model = Task
        fields = ("title",)
