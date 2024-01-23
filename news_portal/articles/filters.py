import django_filters
from .models import Post
from django import forms

class NewsFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    author__user__username = django_filters.CharFilter(lookup_expr='icontains')
    creation_time = django_filters.DateFilter(field_name='creation_time', lookup_expr='gt', widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Post
        fields = ['title', 'author__user__username', 'creation_time']