
from article.models import Comment,Article
from parler.forms import TranslatableModelForm,TranslatedField

class CommentForm(TranslatableModelForm):
    title = TranslatedField()
    body = TranslatedField()
    class Meta:
        model = Comment
        fields = ('body','owner','article',)

class ArticleForm(TranslatableModelForm):
    title = TranslatedField()
    content = TranslatedField()
    category = TranslatedField()
    tags = TranslatedField()

    class Meta:
        model = Article
        fields = ('title','content','category','picture','tags')
    # fields = ['title','content','category','picture','tags']