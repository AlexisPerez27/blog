# Generated by Django 4.2.19 on 2025-02-25 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_categoria_id_alter_heading_id_alter_post_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='descripcion',
            field=models.TextField(blank=True, null=True),
        ),
    ]
