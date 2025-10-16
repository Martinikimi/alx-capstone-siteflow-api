import django_filters
from django.db.models import Q
from .models import Issue

class IssueFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    
    class Meta:
        model = Issue
        fields = ['trade', 'priority', 'status']
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(issue_title__icontains=value) | 
            Q(detailed_description__icontains=value)
        )