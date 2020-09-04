

from django.db import models

# Create your models here.
from django.utils import timezone
from django.utils.timezone import now


class User(models.Model):
    """博客用户表"""
    name = models.CharField(max_length=50,verbose_name="用户名")
    password = models.CharField(max_length=128,verbose_name="用户密码")
    # telphone = models.CharField(max_length=128,verbose_name="用户手机号",null=True)
    email = models.CharField(max_length=128,verbose_name="用户Email",null=True)
    is_superuser = models.BooleanField(default=False,verbose_name="是否是管理员")

    reserved1 = models.CharField(max_length=1024, verbose_name="保留字段1", null=True)
    reserved2 = models.CharField(max_length=1024, verbose_name="保留字段2", null=True)
    reserved3 = models.CharField(max_length=1024, verbose_name="保留字段3", null=True)
    reserved4 = models.CharField(max_length=1024, verbose_name="保留字段4", null=True)



    def __str__(self):
        return self.name

    class Meta:
        db_table = "User"
        verbose_name_plural = '博客用户表'




class Article(models.Model):
    """博客文章"""
    title = models.CharField(max_length=128,verbose_name="文章标题")
    author = models.ForeignKey("User",max_length=128,verbose_name="文章的作者",on_delete=models.CASCADE)
    content = models.TextField(verbose_name="文章的内容")
    view_counter = models.IntegerField(default=0,verbose_name="浏览次数")
    conment_nums = models.IntegerField(verbose_name='评论数', default=0)
    created_time = models.DateField(default=timezone.now,verbose_name="创建时间")
    category = models.ForeignKey("Category",verbose_name="分类",on_delete=models.CASCADE)
    tag = models.ManyToManyField("Tag",verbose_name="标签")

    reserved1 = models.CharField(max_length=1024, verbose_name="保留字段1", null=True)
    reserved2 = models.CharField(max_length=1024, verbose_name="保留字段2", null=True)
    reserved3 = models.CharField(max_length=1024, verbose_name="保留字段3", null=True)
    reserved4 = models.CharField(max_length=1024, verbose_name="保留字段4", null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Article"
        verbose_name_plural = '博客文章表'



class Category(models.Model):
    "文章的分类"
    name = models.CharField(max_length=25,verbose_name="分类名")

    reserved1 = models.CharField(max_length=1024, verbose_name="保留字段1", null=True)
    reserved2 = models.CharField(max_length=1024, verbose_name="保留字段2", null=True)
    reserved3 = models.CharField(max_length=1024, verbose_name="保留字段3", null=True)
    reserved4 = models.CharField(max_length=1024, verbose_name="保留字段4", null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Category"
        verbose_name_plural = '博客分类表'



class Tag(models.Model):
    "文章标签"
    tag_name = models.CharField('标签名', max_length=30)
    created_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now,null=True)
    last_mod_time = models.DateTimeField(verbose_name='修改时间', default=timezone.now,null=True)

    reserved1 = models.CharField(max_length=1024, verbose_name="保留字段1", null=True)
    reserved2 = models.CharField(max_length=1024, verbose_name="保留字段2", null=True)
    reserved3 = models.CharField(max_length=1024, verbose_name="保留字段3", null=True)
    reserved4 = models.CharField(max_length=1024, verbose_name="保留字段4", null=True)

    def __str__(self):
        return self.tag_name

    class Meta:
        db_table = "Tag"
        verbose_name_plural = '博客标签表'



class Comment(models.Model):
    "博客评论表"
    user = models.ForeignKey("User",verbose_name='评论的用户ID', max_length=25,on_delete=models.CASCADE)
    # title = models.CharField(verbose_name="标题", max_length=100)
    Article_id = models.ForeignKey("Article",verbose_name='文章id', max_length=25,on_delete=models.CASCADE)
    conment = models.TextField(verbose_name='评论内容')
    add_time = models.DateTimeField(verbose_name='添加时间', default=timezone.now)

    reserved1 = models.CharField(max_length=1024, verbose_name="保留字段1", null=True)
    reserved2 = models.CharField(max_length=1024, verbose_name="保留字段2", null=True)
    reserved3 = models.CharField(max_length=1024, verbose_name="保留字段3", null=True)
    reserved4 = models.CharField(max_length=1024, verbose_name="保留字段4", null=True)

    class Meta:
        db_table = "Comment"
        verbose_name_plural = '博客评论表'

    def __str__(self):
        return self.conment
