import base64
import hashlib
import json
import random
from datetime import datetime

from django.contrib.auth import authenticate, login
from django.contrib.sessions.models import Session
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from app import models, pagination
from app.function import my_md5
from app.models import User


class LoginView(View):
    """登录视图"""

    def post(self,request):
        try:
            username = request.POST.get("username").strip()
            userpassword = request.POST.get("userpassword").strip()
            print(username)
            print(userpassword)
            if len(username) == 0 or len(userpassword) == 0:
                return HttpResponse(json.dumps({'status': -1, 'response': "参数不能为空,请检查参数."}, ensure_ascii=False))

            user = models.User.objects.filter(name = username)
            if len(user) == 0 :
                print("您还没有注册，请先去注册后登录.")
                return HttpResponse(json.dumps({'status': -1, 'response': "您还没有注册，请先去注册后登录."}, ensure_ascii=False))

            # 登录验证
            userObj_password = models.User.objects.get(name = username).password
            if userpassword == userObj_password :
                # 设置Session.
                # TODO:
                user = list(User.objects.filter(name=username, password=userpassword).values())
                print("user:",user)
                # 用户信息记录在session中
                request.session['user'] = user
                # 创建session,否则key为None
                if not request.session.session_key:
                    request.session.create()
                    # 获取session_key
                key = request.session.session_key
                request.session[key] = user[0]["id"]
                print("key:",request.session[key])
                return HttpResponse(json.dumps({'status': 200, 'response': "用户登录成功.","session":{"sessionID":user[0]["id"],"session_key":key}}, ensure_ascii=False))
            else:
                print("密码错误，请重新输入.")
                return HttpResponse(json.dumps({'status': -1, 'response': "密码错误.请重新输入."}, ensure_ascii=False))
        except:
            return HttpResponse(json.dumps({'status': -1, 'response': "参数异常"}, ensure_ascii=False))


class RegisterView(View):
    """注册"""
    def post(self,request):
        try:
            username = request.POST.get("username").strip()
            userpassword = request.POST.get("userpassword").strip()
            useremail = request.POST.get("useremail").strip()

            if len(username) == 0 or len(userpassword) == 0 or len(useremail) == 0 :
                return HttpResponse(json.dumps({'status': -1, 'response': "参数不能为空,请检查参数."}, ensure_ascii=False))

            user = models.User.objects.filter(name = username)
            if len(user) == 0 :
                try:
                    models.User.objects.create(name=username,password=userpassword,email=useremail,is_superuser=False)
                    return HttpResponse(json.dumps({'status': 200, 'response': "注册成功.请去登录吧."}, ensure_ascii=False))
                except:
                    return HttpResponse(json.dumps({'status': -1, 'response': "注册失败,请检查失败原因."}, ensure_ascii=False))
            else:
                return HttpResponse(json.dumps({'status': 200, 'response': "您已注册成功.不需要重复注册.请去登录吧."}, ensure_ascii=False))

        except:
            return HttpResponse(json.dumps({'status': -1, 'response': "参数异常"}, ensure_ascii=False))



class LoginStatusView(View):

    def post(self,request):
        try:
            sessionID = request.POST.get("sessionID").strip()
            print("sessionID:",eval(sessionID)["session_key"])
            try:
                if request.session.exists(eval(sessionID)["session_key"]):
                    print("sessionID 存在.")
                    return  HttpResponse(json.dumps({'status': 200, 'response': 200}, ensure_ascii=False))
                else:
                    return  HttpResponse(json.dumps({'status': -1, 'response': 0}, ensure_ascii=False))
            except:
                return   HttpResponse(json.dumps({'status': -1, 'response': "session失效."}, ensure_ascii=False))
        except:
            return HttpResponse(json.dumps({'status': -1, 'response': "参数异常"}, ensure_ascii=False))


class LoginoutView(View):
    """退出视图"""
    def post(self,request):
        pass



class ArticleView(View):
    """主页文章列表视图"""
    def get(self,request):
        # 当前页码
        cur_page = request.GET.get("page",1)

        article_list = models.Article.objects.all()
        # 获取当前页
        page_obj = pagination.Pagination(cur_page, article_list.count(), 5)
        articles = article_list[page_obj.start:page_obj.end]
        info_list = []
        for article in articles:
            dict = model_to_dict(article)
            dict["author"] = article.author.name
            dict["content"] = str(article.content)[:100] +' ...' if len(str(article.content)) > 100 else article.content
            dict["created_time"] = article.created_time.strftime("%Y-%m-%d %H:%M:%S")
            del dict["tag"]
            info_list.append(dict)

        page_dict = {}
        page_dict['cur_page'] = cur_page
        page_dict['page_start'] = page_obj.page_start
        page_dict['page_end'] = page_obj.page_end
        page_dict['last_page'] = page_obj.total_page_num
        page_dict['data_count'] = article_list.count()
        info_list.append(page_dict)

        return HttpResponse(json.dumps({'status': 200, 'response': info_list}, ensure_ascii=False))



class BlogDetailView(View):

    def get(self,request):
        """获取文章详情"""
        try:
            paramter = int(request.GET.get("id"))
        except:
            return HttpResponse(json.dumps({'status': -1, 'response': "参数异常"}, ensure_ascii=False))

        article = models.Article.objects.filter(id=paramter).first()
        if article:
            article_dict = model_to_dict(article)
            article_dict["author"] = article.author.name
            article_dict["content"] = article.content
            article_dict["created_time"] = article.created_time.strftime("%Y-%m-%d %H:%M:%S")

            tags =models.Article.objects.get(id= article.id)
            del article_dict["reserved1"],article_dict["reserved2"],article_dict["reserved3"],article_dict["reserved4"]
            article_dict["tag"] = [tag.tag_name for tag in tags.tag.all()]

            return HttpResponse(json.dumps({'status': 200, 'response': article_dict}, ensure_ascii=False))




class ArticleCommon(View):
    """文章评论"""
    def get(self,request):

        # 当前页
        cur_page = request.GET.get("page")
        try:
            paramter = int(request.GET.get("id"))
        except:
            return HttpResponse(json.dumps({'status': -1, 'response': "参数异常"}, ensure_ascii=False))

        comments_Query = models.Comment.objects.filter(Article_id_id=paramter).order_by('-add_time')
        # 获取当前页
        page_obj = pagination.Pagination(cur_page, comments_Query.count(), 5)
        comments = comments_Query[page_obj.start:page_obj.end]
        info = []
        for comment in comments :
            dict = model_to_dict(comment)
            dict["add_time"] = comment.add_time.strftime("%Y-%m-%d %H:%M:%S")
            dict["user"] = comment.user.name
            del dict["reserved1"], dict["reserved2"], dict["reserved3"], dict["reserved4"]
            info.append(dict)
        page_dict = {}
        page_dict['cur_page'] = cur_page
        page_dict['page_start'] = page_obj.page_start
        page_dict['page_end'] = page_obj.page_end
        page_dict['last_page'] = page_obj.total_page_num
        page_dict['data_count'] = comments_Query.count()
        info.append(page_dict)

        return HttpResponse(json.dumps({'status': 200, 'response': info}, ensure_ascii=False))


    def post(self,request):
        """添加一条评论数据"""
        # TODO：待做......
        # session 中的user_ID
        try:
            session_id = request.POST.get("sessionID")
            # 评论内容
            comment_text = request.POST.get("comment_text")
            # 文章ID
            id = request.POST.get("id")
            print(session_id)
            print(comment_text)
            print(id)
            models.Comment.objects.create(Article_id_id=id,user_id=session_id,conment=comment_text,add_time=datetime.now())
            return HttpResponse(json.dumps({'status': 200, 'response': "评论成功!."}, ensure_ascii=False))
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({'status': -1, 'response': "参数异常"}, ensure_ascii=False))