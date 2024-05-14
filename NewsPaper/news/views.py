from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, \
     TemplateView
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm
from .resources import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required


class PostList(ListView):
    model = Post
    template_name = "post_list.html"
    ordering = '-creation_date'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = 'post'


class PostSearch(ListView):
    model = Post
    template_name = 'post_search.html'
    context_object_name = 'posts'
    ordering = ['-creation_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


# Создание новости
class PostCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    success_url = reverse_lazy('news')
    permission_required = ('news.add_post',)

    # permission_required = ('<app>.<action>_<model>',
    # '<app>.<action>_<model>')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category_type = news
        return super().form_valid(form)
        #
        # response = super().form_valid(form)
        # self.success_url = reverse_lazy('post_create', kwargs={'pk': self.object.id})
        # return response


# Редактирование новости
class ProtectedView(LoginRequiredMixin):
    template_name = 'post_edit.html'


class PostUpdate(ProtectedView, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    permission_required = ('news.change_post',)
    # template_name = 'post_edit.html'
    # success_url = reverse_lazy('news')


# Удаление новости
class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news')
    permission_required = ('news.delete_post',)


# Создание статьи
class ArticleCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'
    success_url = reverse_lazy('news')
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category_type = article
        return super().form_valid(form)


# Редактирование статьи
class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'
    permission_required = ('news.change_post',)
    # success_url = reverse_lazy('news')


# Удаление новости
class ArticleDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('news')
    permission_required = ('news.delete_post',)


class CategoryList(PostList):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.post_category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(post_category=self.post_category).order_by('-creation_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.post_category.subscribers.all()
        context['category'] = self.post_category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категории'
    return render(request, 'subscribe.html', {'category': category, 'message': message})
