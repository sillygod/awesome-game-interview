# Generated by Django 2.2.1 on 2019-09-09 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mobile',
            field=models.CharField(default='', max_length=32, unique=True, verbose_name='cell phone num'),
        ),
    ]
