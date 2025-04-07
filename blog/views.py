from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import ModelPost
from .forms import PostForm


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
