# Generated by Django 4.2.19 on 2025-02-25 21:30

import apps.blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_categoria_descripcion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='imagenes',
            field=models.ImageField(blank=True, null=True, upload_to=apps.blog.models.categoria_images_directory),
        ),
    ]
