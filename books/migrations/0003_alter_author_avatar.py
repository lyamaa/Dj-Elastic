# Generated by Django 3.2 on 2021-04-28 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_alter_author_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='author', verbose_name='Author Image'),
        ),
    ]
