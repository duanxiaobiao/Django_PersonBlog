# Generated by Django 2.1.8 on 2020-07-14 12:31

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='文章标题')),
                ('author', models.CharField(max_length=128, verbose_name='文章的作者')),
                ('content', models.TextField(verbose_name='文章的内容')),
                ('view_counter', models.ImageField(default=0, upload_to='', verbose_name='浏览次数')),
                ('conment_nums', models.IntegerField(default=0, verbose_name='评论数')),
                ('created_time', models.DateField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('reserved1', models.CharField(max_length=1024, null=True, verbose_name='保留字段1')),
                ('reserved2', models.CharField(max_length=1024, null=True, verbose_name='保留字段2')),
                ('reserved3', models.CharField(max_length=1024, null=True, verbose_name='保留字段3')),
                ('reserved4', models.CharField(max_length=1024, null=True, verbose_name='保留字段4')),
            ],
            options={
                'verbose_name_plural': '博客文章表',
                'db_table': 'Article',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, verbose_name='分类名')),
                ('reserved1', models.CharField(max_length=1024, null=True, verbose_name='保留字段1')),
                ('reserved2', models.CharField(max_length=1024, null=True, verbose_name='保留字段2')),
                ('reserved3', models.CharField(max_length=1024, null=True, verbose_name='保留字段3')),
                ('reserved4', models.CharField(max_length=1024, null=True, verbose_name='保留字段4')),
            ],
            options={
                'verbose_name_plural': '博客分类表',
                'db_table': 'Category',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conment', models.TextField(verbose_name='评论内容')),
                ('add_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='添加时间')),
                ('reserved1', models.CharField(max_length=1024, null=True, verbose_name='保留字段1')),
                ('reserved2', models.CharField(max_length=1024, null=True, verbose_name='保留字段2')),
                ('reserved3', models.CharField(max_length=1024, null=True, verbose_name='保留字段3')),
                ('reserved4', models.CharField(max_length=1024, null=True, verbose_name='保留字段4')),
                ('Article_id', models.ForeignKey(max_length=25, on_delete=django.db.models.deletion.CASCADE, to='app.Article', verbose_name='文章id')),
            ],
            options={
                'verbose_name_plural': '博客评论表',
                'db_table': 'Comment',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=30, verbose_name='标签名')),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('last_mod_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='修改时间')),
                ('reserved1', models.CharField(max_length=1024, null=True, verbose_name='保留字段1')),
                ('reserved2', models.CharField(max_length=1024, null=True, verbose_name='保留字段2')),
                ('reserved3', models.CharField(max_length=1024, null=True, verbose_name='保留字段3')),
                ('reserved4', models.CharField(max_length=1024, null=True, verbose_name='保留字段4')),
            ],
            options={
                'verbose_name_plural': '博客标签表',
                'db_table': 'Tag',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='用户名')),
                ('password', models.CharField(max_length=128, verbose_name='用户密码')),
                ('telphone', models.CharField(max_length=128, null=True, verbose_name='用户手机号')),
                ('email', models.CharField(max_length=128, null=True, verbose_name='用户Email')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='是否是管理员')),
                ('reserved1', models.CharField(max_length=1024, null=True, verbose_name='保留字段1')),
                ('reserved2', models.CharField(max_length=1024, null=True, verbose_name='保留字段2')),
                ('reserved3', models.CharField(max_length=1024, null=True, verbose_name='保留字段3')),
                ('reserved4', models.CharField(max_length=1024, null=True, verbose_name='保留字段4')),
            ],
            options={
                'verbose_name_plural': '博客用户表',
                'db_table': 'User',
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(max_length=25, on_delete=django.db.models.deletion.CASCADE, to='app.User', verbose_name='评论的用户ID'),
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Category', verbose_name='分类'),
        ),
        migrations.AddField(
            model_name='article',
            name='tag',
            field=models.ManyToManyField(to='app.Tag', verbose_name='标签'),
        ),
    ]
