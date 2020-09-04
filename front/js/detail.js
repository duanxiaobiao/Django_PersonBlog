

// 博客详情页加载
$(function () {
    var url_info = window.location.search.substring(1);
    if (url_info.indexOf('id=') === -1) {
        console.log("系统异常....")
    }

    console.log(url_info);
    $.ajax({
        url: "http://127.0.0.1:8000/detail/?"+url_info,
        type: "GET",
        contentType: "application/json",
        dataType: 'json',
        success: function (json) {
            if (json.status === 200){
                console.log(json.response);
                article = json.response;
                // 详情页的头部信息 header
                var header = '<h2 class="c_titile">'+article.title+'</h2>\n' +
                    '    <p class="box_c"><span class="d_time">发布时间：'+article.created_time+'</span><span>编辑：'+article.author+'</span>' +
                    '     <span>标签：'+article.tag+'</span></p>\n' +
                    '    ';
                $('.index_about').prepend($(header));


                // 详情页的文章内容 content
                var li = '<div>' +article.content +'</div>';
                $('#infos').append($(li))

            }
        },
        error: function () {
            var tr_tag = '<div style="margin-left: 400px;margin-top:50px;"><p>数据获取失败</p></div>';
            $("#bloglist").append(tr_tag);
        }
    });

    //本篇文章的评论渲染
    comment_render(url_info,1);

});

// 评论的HTML 卡片
function comment_card(comment) {
    var comment_wrap = '<li>\n' +
        '          <div class="comment-wrap">\n' +
        '            <div class="photo">\n' +
        '              <div class="avatar" style="background-image: url(\'images/favicon.ico\')"></div>\n' +
        '              <span><strong style="color: blue">'+comment.user+'</strong></span>\n' +
        '            </div>\n' +
        '            <div class="comment-block">\n' +
        '              <p class="comment-text">'+comment.conment+'</p>\n' +
        '              <div class="bottom-comment">\n' +
        '                <div class="comment-date" >'+comment.add_time+'</div>\n' +
        '                <ul class="comment-actions">\n' +
        '                  <li class="complain">Complain</li>\n' +
        '                  <li class="reply">Reply</li>\n' +
        '                </ul>\n' +
        '              </div>\n' +
        '            </div>\n' +
        '          </div>\n' +
        '        </li>';
    $("#comment_card").append($(comment_wrap));
}

function comment_render(url_info,cur_page) {
    $.ajax({
        url: "http://127.0.0.1:8000/article-comments/?"+url_info+'&page='+cur_page,
        type: "GET",
        contentType: "application/json",
        dataType: 'json',
        success: function (json) {
            if (json.status === 200){
                $("#comment_card li").remove();
                var data = json.response;
                var page_info = data.pop();
                pagination(page_info);
                if(data.length === 0){
                    $(".news").attr('hidden',false);
                    $(".news").css('height','100px');
                    $('#comment_card').append($('<p style="color: red" class="comment-message">暂无评论.</ps>'))
                }else{
                    $(".news").css('height','500px');
                    $(".comment-message").remove();
                    $.each(data,function (val,comment) {
                        comment_card(comment);
                    })
                }

            }
        },
        error: function () {
            var tr_tag = '<div style="margin-left: 400px;margin-top:50px;"><p>数据获取失败</p></div>';
            $("#comment_card").append(tr_tag);
        }
    });
}




/**
 * 点击非当前页时触发事件，发送ajax请求,替换数据.
 * */
$('.page_split2').off('click').on("click", '.page_num', function () {
    var url_info = window.location.search.substring(1);
    if (url_info.indexOf('id=') === -1) {
        console.log("系统异常....")
    }

    var cur_page = $(this).attr('page');
    comment_render(url_info,cur_page);

});


/**
 *点击上一页按钮,触发事件.
 * */
$('.page_split').off('click').on("click", '#prev_page_num', function () {
    var url_info = window.location.search.substring(1);
    if (url_info.indexOf('id=') === -1) {
        console.log("系统异常....")
    }

    var cur_page = parseInt($('#cur_page').attr('page')) - 1;
    comment_render(url_info,cur_page);

});


/**
 *点击下一页按钮,触发事件.
 * */
$('#page_split').off('click').on("click", '#next_page_num', function () {
    var url_info = window.location.search.substring(1);
    if (url_info.indexOf('id=') === -1) {
        console.log("系统异常....")
    }

    var cur_page = parseInt($('#cur_page').attr('page')) + 1;
    comment_render(url_info,cur_page);

});

/**
 * 添加评论
 * */
$('.comment-submit').on('click',function () {
    var sessionID = sessionStorage.getItem("session");
    var comment_text = $('#comment-text').val().replace(/^\s+|\s+$/g, "");//去除两边空格
    var id = window.location.search.substring(1).split('=')[1];
    if (sessionID ===null){
        alert("您还没有登录，无法进行评论,请先登录.");
        return 0;
    }
    if (comment_text.length === 0){
        swal("您还有填写评论，请您填写!");
        return 0
    }
    var formData = new FormData();

    formData.append("sessionID",JSON.parse(sessionID)["sessionID"]);
    formData.append("comment_text",comment_text);
    formData.append("id",id);
    // 登录成功后进行评论.
    $.ajax({
        url: "http://127.0.0.1:8000/article-comments/",
        type: "POST",
        data: formData,
        async: false,
        contentType: false,
        timeout: 3000,
        dataType: 'json',
        processData: false,   // jQuery不要去处理发送的数据
        success: function (json) {
            alert(json.response);

            // 刷新数据.
            comment_render('id='+id,1)
        },error:function () {
            console.log("异常....")
        }
    })


});




