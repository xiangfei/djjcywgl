from django_filters import rest_framework as filters
from .models import Asset


class AssetFilter(filters.FilterSet):
    svrfirstusestart = filters.DateFilter(name="svrfirstusetime", lookup_expr='gte')
    svrfirstuseend = filters.DateFilter(name="svrfirstusetime", lookup_expr='lte')
    svrstopstart = filters.DateFilter(name="svrstoptime", lookup_expr='gte')
    svrstopend = filters.DateFilter(name="svrstoptime", lookup_expr='lte')
    svroffstart = filters.DateFilter(name="svrofftime", lookup_expr='gte')
    svroffend = filters.DateFilter(name="svrofftime", lookup_expr='lte')
    sfwname = filters.CharFilter(name="sfwname")

    class Meta:
        model = Asset
        fields = ('svrfirstusestart', 'svrfirstuseend', 'svrstopstart', 'svrstopend', 'svroffstart', 'svroffend')
