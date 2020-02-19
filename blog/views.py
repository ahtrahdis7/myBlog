from django.shortcuts import render,get_list_or_404,redirect
from django.utils import timezone
from blog.models import Post,Comment
from django.contrib.auth.decorators import login_required
from blog.forms import PostForm,CommentForm
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView,ListView,
                                    DetailView,CreateView,
                                    UpdateView,DeleteView,
                                    )
# Create your views here.


class AboutView(TemplateView):
    model = Post
    template_name = 'blog/about.html'

    def get_queryset(self):
        return Post.objects.filter(published_date__lte = timezone.now()).order_by('-published_date')

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte = timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post


class CreatePostView(LoginRequiredMixin,CreateView):

    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin,UpdateView):

    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = '/'
    # redirect_field_name = 'post_draft'

class DraftListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'blog/post_draft.html'
    login_url = '/login/'
    # redirect_field_name = 'post_list'
    
    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('-create_date')


#########################################################################

@login_required
def post_publish(request,pk):
    post = get_list_or_404(Post,pk=pk)
    post[0].publish()
    return redirect('post_detail', pk=pk)

def add_comment_to_post(request,pk):
    pos = get_list_or_404(Post,pk=pk)
    post = pos[0]
    print("Hello am In There")
    if request.method == 'POST':
        form = CommentForm(request.POST)
        print("Hello am In There1")
        if form.is_valid():
            comment = form.save(commit = False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)

    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html',{'form': form})

    


@login_required
def comment_approve(request,pk):
    comment = get_list_or_404(Comment,pk=pk)
    comment[0].approve()

    return redirect('post_detail', pk = comment[0].post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_list_or_404(Comment,pk=pk)
    post_pk = comment[0].post.pk
    comment[0].delete()
    return redirect('post_detail', pk=post_pk)





