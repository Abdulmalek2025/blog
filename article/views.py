from django.conf import LazySettings
from django.shortcuts import render
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormMixin
from django.views.generic import DetailView, RedirectView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from .models import Article, Category, Comment,ArticleTranslation,CategoryTranslation,CommentTranslation
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.db.models import Count
from django import forms
from django.db.models import Q
import random
from article.forms import CommentForm,ArticleForm
from parler.views import TranslatableCreateView,TranslatableUpdateView,ViewUrlMixin

class HomeView(TemplateView):
    template_name = 'article/index.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context['slide'] = ArticleTranslation.objects.filter(language_code=self.request.LANGUAGE_CODE).last()
        context['popular'] = ArticleTranslation.objects.filter(language_code=self.request.LANGUAGE_CODE).order_by('-id')[:4]
        context['recent'] = ArticleTranslation.objects.filter(language_code=self.request.LANGUAGE_CODE).order_by('views')[:2]
        trending = list(ArticleTranslation.objects.filter(language_code=self.request.LANGUAGE_CODE))
        count = ArticleTranslation.objects.filter(language_code=self.request.LANGUAGE_CODE).count()
        if count >4:
            context['trending'] = random.sample(trending,4)
            context['inspire'] = random.sample(trending,4)
        else:
            context['trending'] = random.sample(trending,count)
            context['inspire'] = random.sample(trending,count)
        context['categories'] = Category.objects.all().annotate(articles=Count('articletranslation'))
        return context

class ArticleListView(ViewUrlMixin,ListView):
    model = ArticleTranslation
    paginate_by = 2
    view_url_name = 'category'
    def get_queryset(self, *args, **kwargs):
        
        return super().get_queryset(*args, **kwargs).filter(
            category=self.request.GET.get('category','lifestyle')
        )
    def get_context_data(self, *args, **kwargs):
        context = super(ArticleListView,
             self).get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all().annotate(articles=Count('articletranslation'))
        # add extra field        
        return context    

class ArticleCounterView(RedirectView):

    permanent = False
    query_string = True
    pattern_name = 'article:detail'

    def get_redirect_url(self, *args, **kwargs):
        article = get_object_or_404(ArticleTranslation, master_id=kwargs['pk'])
        article.views += 1
        article.save()
        return super().get_redirect_url(*args, **kwargs)

class ArticleDetailView(FormMixin,DetailView):
    model = Article
    template_name = "article/article_detail.html"
    form_class = CommentForm
    def get_queryset(self, *args, **kwargs):
        
        return super().get_queryset(*args, **kwargs)
    
    def get_success_url(self):
        return reverse('article:detail', kwargs={'pk': self.object.id})

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleDetailView,
             self).get_context_data(*args, **kwargs)
        # add extra field 
        context['categories'] = Category.objects.all().annotate(articles=Count('articletranslation'))
        context["tags"] = self.object.tags.split(',')
        context['form'] = CommentForm(initial={'article': self.object,'owner':self.request.user.pk})
        context['form'].fields['owner'].widget = forms.HiddenInput()
        context['form'].fields['article'].widget = forms.HiddenInput()
        context['comments'] =  CommentTranslation.objects.filter(article=self.object).order_by('-id')
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
class ArticleCreateView(TranslatableCreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article/article_form.html'
    def get_success_url(self):
        return reverse('article:detail', args=[self.object.pk])
    def get_form_language(self):
        return self.request.LANGUAGE_CODE
    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        return super().form_valid(form)
    def get_context_data(self, *args, **kwargs):
        context = super(ArticleCreateView,
             self).get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all().annotate(articles=Count('articletranslation'))
        # add extra field        
        return context

@method_decorator(login_required(), name='dispatch')
class ArticleUpdateView(TranslatableUpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article/article_form.html'
    def get_success_url(self):
        return reverse('article:index')

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleUpdateView,
             self).get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all().annotate(articles=Count('articletranslation'))
        # add extra field        
        return context    

@method_decorator(login_required(),name='dispatch')
class DeleteArticleView(DeleteView):
    model = Article
    template_name = 'article/article_delete_confirm.html'
    success_url = reverse_lazy('article:index')
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner_id == request.user.id:
            self.object.delete()
            return redirect(self.get_success_url())
        else:
            return reverse_lazy('article:detail',self.object.id)
    def get_context_data(self, *args, **kwargs):
        context = super(DeleteArticleView,
             self).get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all().annotate(articles=Count('articletranslation'))
        # add extra field        
        return context    

    
class CategoryList(ViewUrlMixin,ListView):
    model = ArticleTranslation
    template_name = 'article/article_list.html'
    paginate_by = 2
    view_url_name = 'article:category'
    def get_queryset(self, *args, **kwargs):
 
        return super().get_queryset(*args, **kwargs).filter(
            category_id=CategoryTranslation.objects.values('master_id').filter(name=self.request.GET.get('category'))[:1],language_code=self.request.LANGUAGE_CODE)
        
    def get_context_data(self, *args, **kwargs):
        context = super(CategoryList,
             self).get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all().annotate(articles=Count('articletranslation')/2)
        # add extra field        
        return context  

class SearchView(ListView):
    
    model = ArticleTranslation
    paginate_by = 2
    template_name = 'article/search_result.html'
    def get_queryset(self, *args, **kwargs):
 
        return super().get_queryset(*args, **kwargs).filter(
            Q(content__contains=self.request.GET.get('search'))|
            Q(title__contains=self.request.GET.get('search'))|
            Q(short_description__contains=self.request.GET.get('search'))|
            Q(tags__contains=self.request.GET.get('search')))
        
    def get_context_data(self, *args, **kwargs):
        context = super(SearchView,
             self).get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all().annotate(articles=Count('articletranslation'))
        context['keyword'] = self.request.GET.get('search')
        # add extra field        
        return context

class MyArticle(ViewUrlMixin,ListView):
    model = ArticleTranslation
    template_name = 'article/article_user.html'
    view_url_name = 'mine'
    paginate_by = 2
    def get_queryset(self, *args, **kwargs):
        
        return super().get_queryset(*args, **kwargs).filter(
            owner=self.request.user,language_code=self.request.LANGUAGE_CODE
        )


