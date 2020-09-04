# Generated by Django 2.1.8 on 2020-07-14 12:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='created_time',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='last_mod_time',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='修改时间'),
        ),
    ]
