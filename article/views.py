from django.shortcuts import render
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormMixin
from django.views.generic import DetailView, RedirectView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from .models import Article, Category, Comment
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.db.models import Count
from django import forms
from django.db.models import Q
import random
from article.forms import CommentForm

class HomeView(TemplateView):
    template_name = 'article/index.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context['slide'] = Article.objects.only('title','category','owner','created_at').last()
        context['popular'] = Article.objects.order_by('views')[:4]
        context['recent'] = Article.objects.order_by('id')[:4]
        trending = list(Article.objects.all())
        context['trending_large'] = random.sample(trending,2)
        context['trending_small'] = random.sample(trending,4)
        context['inspire'] = random.sample(trending,4)
        context['categories'] = Category.objects.all().annotate(articles=Count('article'))
        return context

class ArticleListView(ListView):
    model = Article
    paginate_by = 2
    def get_queryset(self, *args, **kwargs):
 
        return super().get_queryset(*args, **kwargs).filter(
            category=self.request.GET.get('category')
        )
    def get_context_data(self, *args, **kwargs):
        context = super(ArticleListView,
             self).get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all().annotate(articles=Count('article'))
        # add extra field        
        return context    

class ArticleCounterView(RedirectView):

    permanent = False
    query_string = True
    pattern_name = 'article:detail'

    def get_redirect_url(self, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs['pk'])
        article.update_views()
        return super().get_redirect_url(*args, **kwargs)

class ArticleDetailView(FormMixin,DetailView):
    model = Article
    template_name = "article/article_detail.html"
    form_class = CommentForm

    def get_success_url(self):
        return reverse('article:detail', kwargs={'pk': self.object.id})

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleDetailView,
             self).get_context_data(*args, **kwargs)
        # add extra field 
        context['categories'] = Category.objects.all().annotate(articles=Count('article'))
        context["tags"] = self.object.tags.split(',')
        context['form'] = CommentForm(initial={'article': self.object,'owner':self.request.user.pk})
        context['form'].fields['owner'].widget = forms.HiddenInput()
        context['form'].fields['article'].widget = forms.HiddenInput()
        context['comments'] =  Comment.objects.filter(article=self.object).order_by('-id')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(ArticleDetailView, self).form_valid(form)

@method_decorator(login_required(), name='dispatch')
class ArticleCreateView(CreateView):
    model = Article
    fields = ['title','content','category','picture','tags']
    def get_success_url(self):
        return reverse('article:detail', args=[self.object.pk])
    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        return super().form_valid(form)
    def get_context_data(self, *args, **kwargs):
        context = super(ArticleCreateView,
             self).get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all().annotate(articles=Count('article'))
        # add extra field        
        return context

@method_decorator(login_required(), name='dispatch')
class ArticleUpdateView(UpdateView):
    model = Article
    fields = ['title','content','category','picture','tags']
    def get_success_url(self):
        return reverse('article:list')
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            owner=self.request.user
        )
    def get_context_data(self, *args, **kwargs):
        context = super(ArticleUpdateView,
             self).get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all().annotate(articles=Count('article'))
        # add extra field        
        return context    

@method_decorator(login_required(),name='dispatch')
class DeleteArticleView(DeleteView):
    model = Article
    template_name = 'article/article_delete_confirm.html'
    success_url = reverse_lazy('article:list')
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            owner=self.request.user
        )
    def get_context_data(self, *args, **kwargs):
        context = super(DeleteArticleView,
             self).get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all().annotate(articles=Count('article'))
        # add extra field        
        return context    

    
class CategoryList(ListView):
    model = Article
    paginate_by = 2
    def get_queryset(self, *args, **kwargs):
 
        return super().get_queryset(*args, **kwargs).filter(
            category__name__contains=self.kwargs['category'])
        
    def get_context_data(self, *args, **kwargs):
        context = super(CategoryList,
             self).get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all().annotate(articles=Count('article'))
        # add extra field        
        return context  

class SearchView(ListView):
    
    model = Article
    paginate_by = 2
    template_name = 'article/search_result.html'
    def get_queryset(self, *args, **kwargs):
 
        return super().get_queryset(*args, **kwargs).filter(
            Q(category__name__contains=self.request.GET.get('search'))|Q(title__contains=self.request.GET.get('search'))|Q(short_description__contains=self.request.GET.get('search')))
        
    def get_context_data(self, *args, **kwargs):
        context = super(SearchView,
             self).get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all().annotate(articles=Count('article'))
        context['keyword'] = self.request.GET.get('search')
        # add extra field        
        return context     


