var obj=null;
var As=document.getElementById('topnav').getElementsByTagName('a');
obj = As[0];
for(i=1;i<As.length;i++){if(window.location.href.indexOf(As[i].href)>=0)
obj=As[i];}
obj.id='logout';

// 博客文章的卡片
function article_list(article){
    var li = '<div class="ul-div"><h3 class="'+article.id+'">'+article.title+'</h3>' +
        '    <figure>' +
        '      <img src="images/001.png">' +
        '    </figure>' +
        '    <ul>' +
        '      <p>'+article.content+'</p>' +
        '      <a title="/" href="new.html?id='+article.id+'" target="_blank" class="readmore">阅读全文>></a>\n' +
        '    </ul>' +
        '    <p class="dateview">' +
        '      <span>'+article.created_time+'</span>' +
        '      <span>'+article.author+'</span>' +
        '      <span>个人博客：[<a href="/news/life/">程序人生</a>]</span>' +
        '    </p></div>';
    $('#bloglist').prepend($(li));
}

// 首页加载博客文章列表
$(function () {
   $.ajax({
       url: "http://127.0.0.1:8000/article/",
       type: "GET",
       contentType: "application/json",
       timeout: 3000,
       dataType: 'json',
       success: function (data) {
           if (data.status === 200){
               articles = data.response;
                var page_info = articles.pop();
                pagination(page_info);
                $.each(articles,function (val,article) {
                    article_list(article);
                })
           }
       },
       error: function () {
           var tr_tag = '<div style="margin-left: 400px;margin-top:50px;"><p>数据获取失败</p></div>';
           $("#bloglist").append(tr_tag);
       }
   })
});

/**
 * 点击非当前页时触发事件，发送ajax请求,替换数据.
 * */
$('.page_split2').off('click').on("click", '.page_num', function () {

    var cur_page = $(this).attr('page');
    data_render(cur_page);

});


/**
 *点击上一页按钮,触发事件.
 * */
$('.page_split').off('click').on("click", '#prev_page_num', function () {
    var cur_page = parseInt($('#cur_page').attr('page')) - 1;
    data_render(cur_page);

});


/**
 *点击下一页按钮,触发事件.
 * */
$('#page_split').off('click').on("click", '#next_page_num', function () {

    var cur_page = parseInt($('#cur_page').attr('page')) + 1;
    data_render(cur_page);

});



function data_render(cur_page){

    $.ajax({
        url: "http://127.0.0.1:8000/article/?page="+cur_page,
        type: "GET",
        contentType: "application/json",
        timeout: 3000,
        dataType: 'json',
        success: function (data) {
            if (data.status === 200){
                console.log(data);
                var datas = data.response;
                var page_info = datas.pop();
                pagination(page_info);
                // 清除文章列表，重新加载.
                $(".ul-div").remove();
                $.each(datas,function (val,article) {
                    article_list(article);
                })
            }

        },error : function(e){

        }
    });
}

function login(){
   //登录按钮触发事件
    alert(111)
    $("#modal-content div").remove();

    var login_string = '<div class="modal-header">\n' +
        '        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">\n' +
        '          &times;\n' +
        '        </button>\n' +
        '        <h4 class="modal-title" id="myModalLabel">\n' +
        '          登录\n' +
        '        </h4>\n' +
        '      </div>\n' +
        '      <div class="modal-body" style="text-align: center">\n' +
        '        <p>用户：<input type="text" id="username" style="width: 200px;height: 30px;"></p>\n' +
        '        <p>密码：<input type="password" id="userpassword" style="width: 200px;height: 30px;"></p>\n' +
        '      </div>\n' +
        '      <div class="modal-footer">\n' +
        '        <a href="javascript:void(0);" id="register" onclick="register()" style="float: left;">去注册\n</a>' +
        '        </a>\n' +
        '        <button type="button" class="btn btn-primary" id="login-sumit" onclick="login_submit()">\n' +
        '          登录\n' +
        '        </button>\n' +
        '      </div>'
    $("#modal-content").append($(login_string));

}


// 登录确定按钮
function login_submit() {

    var username = $("#username").val().replace(/^\s+|\s+$/g, "");//去除两边空格;
    var userpassword = $("#userpassword").val().replace(/^\s+|\s+$/g, "");//去除两边空格;

    if(username.length === 0 || userpassword.length === 0 ) {
        if (username.length === 0) {
            alert("用户名不能为空.");
            return 0
        } else if (userpassword.length === 0) {
            alert("密码不能为空");
            return 0

        }
    }
    /** 由于着急写后面的功能，目前只做此检查，以后有时间完善功能。**/
    var formData = new FormData();
    formData.append("username", username);
    formData.append("userpassword", userpassword);

    // 发送Ajax请求.
    $.ajax({
        url: "http://127.0.0.1:8000/login/",
        type: "POST",
        data: formData,
        async: false,
        contentType: false,
        timeout: 3000,
        dataType: 'json',
        processData: false,   // jQuery不要去处理发送的数据
        success: function (json) {
            if(json.status === 200){
                if (json.session){

                    sessionStorage.setItem("session", JSON.stringify(json.session).toString());
                    user_status(JSON.stringify(json.session).toString());
                    // 登录成功后，模态框消失。
                    $("#myModal").modal('hide');
                    $("#login span").remove();
                    var a = "<span>在线</span><span class=\"en\">在线</span>";
                    $("#login").append($(a));
                }
            }else{
                alert(json.response)
            }
        }, error: function () {
            console.log("系统异常....")
        }
    });
}



// 注册按钮
function register() {

    $("#modal-content div").remove();
    var register_string = '<div class="modal-header">\n' +
       '        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">\n' +
       '          &times;\n' +
       '        </button>\n' +
       '        <h4 class="modal-title" id="myModalLabel">\n' +
       '          注册\n' +
       '        </h4>\n' +
       '      </div>\n' +
       '      <div class="modal-body" style="text-align: center">\n' +
       '        <p>用户：<input type="text" id="username" style="width: 200px;height: 30px;"></p>\n' +
       '        <p>密码：<input type="password" id="userpassword" style="width: 200px;height: 30px;"></p>\n' +
       '        <p>邮箱：<input type="text" id="useremail" style="width: 200px;height: 30px;"></p>\n' +
       '      </div>\n' +
       '      <div class="modal-footer">\n' +
       '        <a  href="javascript:void(0);" id="login" style="float: left" onclick="login_render()">去登录</a>' +
       '        <button type="button" class="btn btn-default" id="register-submit" onclick="register_submit()">注册\n' +
       '        </button>\n' +
       '      </div>';
    $("#modal-content").append($(register_string));
    // $(this).attr("data-toggle","modal");
    // $(this).attr("data-target","#myModal");
}

function login_render(){
    //登录按钮触发事件
    $("#modal-content div").remove();

    var login_string = '<div class="modal-header">\n' +
        '        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">\n' +
        '          &times;\n' +
        '        </button>\n' +
        '        <h4 class="modal-title" id="myModalLabel">\n' +
        '          登录\n' +
        '        </h4>\n' +
        '      </div>\n' +
        '      <div class="modal-body" style="text-align: center">\n' +
        '        <p>用户：<input type="text" id="username" style="width: 200px;height: 30px;"></p>\n' +
        '        <p>密码：<input type="password" id="userpassword" style="width: 200px;height: 30px;"></p>\n' +
        '      </div>\n' +
        '      <div class="modal-footer">\n' +
        '        <a href="javascript:void(0);" id="register" onclick="register()" style="float: left;">去注册</a>' +
        '        </a>\n' +
        '        <button type="button" class="btn btn-primary" id="login-sumit" onclick="login_submit()">\n' +
        '          登录\n' +
        '        </button>\n' +
        '      </div>'
    $("#modal-content").append($(login_string));
}


function register_submit(){
    // 注册提交按钮
    var username = $("#username").val().replace(/^\s+|\s+$/g, "");//去除两边空格;
    var userpassword = $("#userpassword").val().replace(/^\s+|\s+$/g, "");//去除两边空格;
    var useremail = $("#useremail").val().replace(/^\s+|\s+$/g, "");//去除两边空格;
    if(username.length === 0 || userpassword.length === 0 || useremail.length ===0){
        if(username.length === 0){
            alert("用户名不能为空.");
            return 0
        }else if(userpassword.length === 0){
            alert("密码不能为空");
            return 0
        }else{
            alert("邮箱不能为空");
            return 0
        }
    }

    /** 由于着急写后面的功能，目前只做此检查，以后有时间完善功能。**/
    var formData = new FormData();
    formData.append("username",username);
    formData.append("userpassword",userpassword);
    formData.append("useremail",useremail);

    $.ajax({
        url: "http://127.0.0.1:8000/register/",
        type: "POST",
        data: formData,
        async: false,
        contentType: false,
        timeout: 3000,
        dataType: 'json',
        processData: false,   // jQuery不要去处理发送的数据
        success: function (json) {
            if (json.status ===200){
                alert(json.response)
            }else{
                alert(json.response)
            }

        },error:function () {
            console.log("系统异常....")
        }
    });

}






$("#logout").click(function () {
    //退出按钮触发事件
    alert(1)
});

function user_status(sessionID) {
    var formData = new FormData();
    formData.append("sessionID",sessionID);
    $.ajax({
        url: "http://127.0.0.1:8000/login-status/",
        type: "POST",
        data: formData,
        async: false,
        contentType: false,
        timeout: 3000,
        dataType: 'json',
        processData: false,   // jQuery不要去处理发送的数据
        success: function (json) {
            console.log(json);
            if(json.status === 200 && json.response === 200){

                $("#login span").remove();

                var a = "<span>在线</span><span class=\"en\">在线</span>";
                $("#login").append($(a));
                $('#login').attr('id','online');
            }else {
                // alert("用户状态:离线");
                $("#online span").remove();
                var a = "<span onclick=\"login()\" data-toggle=\"modal\" data-target=\"#myModal\">登录</span><span class=\"en\">Login</span>";
                $("#online").append($(a));
                $('#online').attr('id','login')
            }

        }
    })

}

$(function () {
   var sessionID =sessionStorage.getItem("session");
   console.log(sessionID);
   user_status(sessionID);
});



