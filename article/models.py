from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from ckeditor_uploader.fields import RichTextUploadingField
from parler.models import TranslatableModel, TranslatedFields
# Create your models here.

class Category(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=255),
        created_at = models.DateField()
    )
    

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name

class Article(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(max_length=255),
        content = RichTextUploadingField(),
        short_description = models.CharField(max_length=255,default='',null=True),
        created_at = models.DateTimeField(default=timezone.now),
        picture = models.ImageField(upload_to="pictures/"),
        category = models.ForeignKey(Category,on_delete=models.CASCADE),
        owner = models.ForeignKey(User,on_delete=models.CASCADE),
        views = models.IntegerField(default=1),
        tags = models.CharField(max_length=255)
    )
    

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title
    def update_views(self):
        self.views = self.views+1
        self.save()

class Comment(TranslatableModel):
    translations = TranslatedFields(
        owner = models.ForeignKey(User,on_delete=models.CASCADE),
        article = models.ForeignKey(Article,on_delete=models.CASCADE),
        body = models.CharField(max_length=255),
        created_at = models.DateTimeField(auto_now_add=True)
    )
    
    
    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return self.body

    def get_absolute_url(self):
        return reverse("Comment_detail", kwargs={"pk": self.pk})






