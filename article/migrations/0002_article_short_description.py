# Generated by Django 4.1.2 on 2022-10-08 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='short_description',
            field=models.CharField(default='', max_length=255, null=True),
        ),
    ]
