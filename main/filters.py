import django_filters
from .models import Content
from django.db.models import Q


class ContentFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Content
        fields = ['body', 'title', 'summary', 'category']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) |
            Q(body__icontains=value) |
            Q(summary__icontains=value) |
            Q(category__icontains=value) 
        )