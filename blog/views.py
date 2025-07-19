from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import ModelPost
from .forms import PostForm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import PostSerializer

# Create your views here.


class PostListView(ListView):
    model = ModelPost
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    queryset = ModelPost.objects.filter(
        published=True).order_by('-published_date')
    paginate_by = 5


class PostDetailView(DetailView):
    model = ModelPost
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_post(self):
        return get_object_or_404(ModelPost, slug=self.kwargs['slug'])


class PostCreateView(CreateView):
    model = ModelPost
    template_name = 'blog/post_form.html'
    form_class = PostForm
    success_url = reverse_lazy('post_list')


class PostUpdateView(UpdateView):
    model = ModelPost
    template_name = 'blog/post_form.html'
    form_class = PostForm
    success_url = reverse_lazy('post_list')


class PostDeleteView(DeleteView):
    model = ModelPost
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')


@require_POST
@login_required
def post_like(request, slug):
    post = get_object_or_404(ModelPost, slug)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)

    return JsonResponse({'likes': post.likes.count()})


class PostViewSet(viewsets.ModelViewSet):
    queryset = ModelPost.objects.filter(published=True)
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        if user in post.like.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)
        return Response({'likes': post.likes.count()})
