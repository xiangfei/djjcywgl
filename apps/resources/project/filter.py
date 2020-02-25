import django_filters
from .models import ProjectRecord, ModuleRecord


class ProjectFilter(django_filters.rest_framework.FilterSet):

    dateold = django_filters.NumberFilter(name="date_joined", lookup_expr='gte')
    datenew = django_filters.NumberFilter(name="date_joined", lookup_expr='lte')

    class Meta:
        model = ProjectRecord
        fields = ('dateold', 'datenew', 'organizational_id', 'department_id')


class ModuleFilter(django_filters.rest_framework.FilterSet):

    dateold = django_filters.NumberFilter(name="date_joined", lookup_expr='gte')
    datenew = django_filters.NumberFilter(name="date_joined", lookup_expr='lte')

    class Meta:
        model = ModuleRecord
        fields = ('dateold', 'datenew', 'child_of_project', 'is_public')
