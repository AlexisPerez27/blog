# Generated by Django 4.2.19 on 2025-02-26 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_postanalytics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='heading',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='headings', to='blog.post'),
        ),
        migrations.AlterField(
            model_name='postanalytics',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_analytics', to='blog.post'),
        ),
        migrations.AlterField(
            model_name='postview',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postview', to='blog.post'),
        ),
    ]
