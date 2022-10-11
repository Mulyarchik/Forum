# Generated by Django 4.1 on 2022-10-11 14:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('backends', '0008_remove_commenttoanswer_comment_to_answer_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=1000, verbose_name='Content')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Asked')),
                ('author', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='backends.question')),
                ('reply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Replies', to='backends.comment')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
        ),
        migrations.RemoveField(
            model_name='commenttoanswer',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='commenttoanswer',
            name='author',
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
        migrations.DeleteModel(
            name='CommentToAnswer',
        ),
    ]
