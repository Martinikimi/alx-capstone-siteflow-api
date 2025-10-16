import django_filters
from django.db.models import Q
from .models import Comment, Issue 

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
        
class CommentFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    issue_id = django_filters.NumberFilter(field_name='issue__id')
    user_id = django_filters.NumberFilter(field_name='user__id')
    date = django_filters.ChoiceFilter(
        method='filter_date',  
        choices=[  
            ('today', 'Today'),
            ('yesterday', 'Yesterday'), 
            ('week', 'Last 7 days'),
            ('month', 'Last 30 days')
        ]
    )
    
    class Meta:
        model = Comment  # This filter works on Comment model
        fields = ['issue_id', 'user_id']  # These fields can be filtered directly
    
    # 👇 CUSTOM SEARCH METHOD - HOW TO SEARCH COMMENT TEXT
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(content__icontains=value)  # Search in comment content
        )
        # What it does: When you search "safety", it finds comments containing "safety"
    
    #  CUSTOM DATE FILTERING METHOD
    def filter_date(self, queryset, name, value):
        today = timezone.now().date()  # Get today's date
        
        #  FILTER FOR TODAY'S COMMENTS
        if value == 'today':
            return queryset.filter(timestamp__date=today)
            # What it does: Show only comments from today
        
        #  FILTER FOR YESTERDAY'S COMMENTS  
        elif value == 'yesterday':
            yesterday = today - timedelta(days=1)
            return queryset.filter(timestamp__date=yesterday)
            # What it does: Show only comments from yesterday
        
        #  FILTER FOR LAST WEEK'S COMMENTS
        elif value == 'week':
            week_ago = today - timedelta(days=7)
            return queryset.filter(timestamp__date__gte=week_ago)
            # What it does: Show comments from last 7 days
        
        # FILTER FOR LAST MONTH'S COMMENTS
        elif value == 'month':
            month_ago = today - timedelta(days=30)
            return queryset.filter(timestamp__date__gte=month_ago)
            # What it does: Show comments from last 30 days
        
        return queryset  # If no date filter, return all comments