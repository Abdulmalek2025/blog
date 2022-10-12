from .models import Category, Article,Comment
from django.contrib import admin
from parler.admin import TranslatableAdmin
# Register your models here.

admin.site.register(Article,TranslatableAdmin)
admin.site.register(Category,TranslatableAdmin)
admin.site.register(Comment,TranslatableAdmin)