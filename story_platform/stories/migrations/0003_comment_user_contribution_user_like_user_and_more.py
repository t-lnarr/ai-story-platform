# Generated by Django 5.1.3 on 2025-03-12 05:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0002_story_text_comment_like'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contribution',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='like',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contribution',
            name='story',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contributions', to='stories.story'),
        ),
        migrations.AlterField(
            model_name='contribution',
            name='user_input',
            field=models.TextField(max_length=200),
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('story', 'user')},
        ),
    ]
