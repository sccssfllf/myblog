from django.shortcuts import render
from django.views.generic import ListView
from .models import ModelPost

# Create your views here.


class PostListView(ListView):
    model = ModelPost
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    queryset = ModelPost.objects.filter(
        published=True).order_by('-published_date')
    paginate_by = 5
