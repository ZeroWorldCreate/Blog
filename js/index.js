// ajax URL声明
var url_check = 'http://172.37.207.157:2000/check';
var url_sub = 'http://172.37.207.157:3000/register';
var url_login = 'http://172.37.207.157:3000/login';
var url_index = 'http://172.37.207.157:3000';
var ifEmail = /^([a-zA-Z]|[0-9])(\w|\-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$/;
var isImage = /^image\/\w+$/;
var headimgData;


function Update_Page(what_Page, isAdmin, isShade) { //ajax获取页面
    if (isAdmin == false) {
        G_url = './html/' + what_Page;
    }
    else if (isAdmin == true) {
        G_url = './admin/' + what_Page;
    };
    if (isShade == false) {
        $.ajax({
            url: G_url,
            success: function (date) {
                $('#PageContext').css({ 'top': 500 });
                $('#PageContext').html(date);

                $('#PageContext').animate({
                    'top': '0'
                }, 500);
            },
        });
    }
    else if (isShade == true) {
        $.ajax({
            url: G_url,
            success: function (date) {
                $('#shade').css({ 'display': 'block', 'opacity': '0' });
                $('#shade').html(date);
                $('#shade').animate({
                    'opacity': '1'
                }, 200);
            },
        });
    };
};

function uploadImg() {
    var fileImg = $('#uploadImg');
    if (fileImg.val()) {
        if (fileImg.length == 1) {
            headimgData = fileImg[0].files[0];
            if (isImage.test(headimgData.type)) {
                Update_Page('editHeadimg.html', false, true)
            }
            else {
                mdui.snackbar({
                    message: '似乎不能提交除图片外的文件呢~(；д；)',
                    position: 'bottom'
                });
            };
        }
        else {
            mdui.snackbar({
                message: "一次只能选择一张图片(〃'▽'〃)",
                position: 'bottom'
            });
        };
    }
    else {
        mdui.snackbar({
            message: '选择的文件不能为空ヽ(￣▽￣)ﾉ',
            position: 'bottom'
        });
    };
    // console.log(headimgData);
};

function index(){
    $.ajax({
        type:'post',
        url: url_index
    });
}

function Verify() { //注册页面验证提交
    var pwd_first = $('#pwd_first').val();
    var pwd_second = $('#pwd_second').val();
    if (pwd_first != '' && pwd_second != '') {
        $('#d_first_pwd').removeClass('mdui-textfield-invalid');
        if (pwd_first != pwd_second) {  //判断两次密码是否输入一致
            $('#d_second_pwd').addClass('mdui-textfield-invalid');
        }
        else {  //下一步判断：判断邮箱是否合法
            $('#d_second_pwd').removeClass('mdui-textfield-invalid');
            if (!$('#d_Email').hasClass('mdui-textfield-invalid')) {    //合法执行下一步判断：用户名是否被注册
                var username = $('#username').val();
                var pwd = $('#pwd_second').val();
                var email = $('#Email').val();
                //查询此用户名是否被注册
                $.ajax({
                    type: 'get',
                    url: url_check,
                    data: { 'username': username },
                    success: function (data) {
                        //alert(data.message);
                        if (data.message == 'ok') {  //未被注册
                            $('#d_Username').removeClass('mdui-textfield-invalid');
                            $.ajax({
                                type: 'post',
                                url: url_sub,
                                data: {
                                    'username': username,
                                    'pwd': pwd,
                                    'Email': email,
                                    'Token': data.token
                                },
                                success: function (data) {
                                    if (data.message == 'ok') {
                                        //注册成功
                                        mdui.snackbar({
                                            message: '注册成功！(￣▽￣)／，我们将会发送一封邮件给您:)',
                                            position: 'bottom'
                                        });
                                    }
                                    else if (data.message == 'error') {
                                        //注册失败
                                        mdui.snackbar({
                                            message: data.why,
                                            position: 'bottom'
                                        });
                                    }
                                    else {
                                        //内部错误
                                        alert('内部错误！');
                                    };
                                },
                                error: function () {
                                    mdui.snackbar({
                                        message: "服务器走丢啦，客官一会再来~(〃'▽'〃)",
                                        position: 'bottom'
                                    });
                                },
                            });
                        }
                        else if (data.message == 'error') {  //被注册
                            $('#d_Username').addClass('mdui-textfield-invalid');
                        }
                        else {   //异常内部
                            alert('内部错误！');
                        };
                    },
                    error: function () {
                        alert('服务器错误！')
                    },
                    dataType: 'json',
                });
            };
        };
    }
    else {
        $('#d_first_pwd').addClass('mdui-textfield-invalid');
    }
};

function login() {  //登录页面提交
    var U_Ename = $('#U_Ename').val();
    var pwd = $('#pwd').val();
    if (U_Ename != '' && pwd != '') {    //账号密码填写完毕，可以提交
        pwd = sha256_digest(pwd);
        //alert(pwd)
        if (ifEmail.test(U_Ename)) {     //真：输入的是邮箱
            //邮箱提交格式
            $.ajax({
                type: 'post',
                url: url_login,
                data: {
                    'username': U_Ename,
                    'pwd': pwd,
                    'type': 'Email',
                },
                success: function (data) {
                    if (data.message == 'ok') {
                        mdui.snackbar({
                            message: "欢迎回来~*(〃'▽'〃)@" + data.user + "<br />[页面3秒后自动跳转]",
                            position: 'bottom',
                        });
                        $('#applyTitle').text(("Alimo1029's Bugs - @" + data.user));
                        $('#handleUser').html($('#userHtml').html());
                        targetPath = ("users/" + data.user + "/headimg/headimg.jpg");
                        alert(targetPath)
                        $('div [id=headimg]').each(function () {
                            $(this).attr('src', targetPath);
                        });
                        setTimeout(function () {
                            Update_Page('index.html', false, false);
                        }, 3000);
                    }
                    else if (data.message == 'error') {
                        //登录失败
                        mdui.snackbar({
                            message: data.why,
                            position: 'bottom',
                        });
                    }
                    else {
                        //内部错误
                        alert('内部错误')
                    };
                },
                error: function () {
                    mdui.snackbar({
                        message: "服务器走丢啦，客官一会再来~(〃'▽'〃)",
                        position: 'bottom',
                    });
                },
            });
        }
        else {   //假：输入的是用户名
            //用户名提交格式
            $.ajax({
                type: 'post',
                url: url_login,
                data: {
                    'username': U_Ename,
                    'pwd': pwd,
                    'type': 'user',
                },
                success: function (data) {
                    if (data.message == 'ok') {
                        mdui.snackbar({
                            message: "欢迎回来~*(〃'▽'〃)@" + data.user + "<br />[页面3秒后自动跳转]",
                            position: 'bottom',
                        });
                        $('#applyTitle').text(("Alimo1029's Bugs - @" + data.user));
                        $('#handleUser').html($('#userHtml').html());
                        targetPath = ("users/" + data.user + "/headimg/headimg.jpg");
                        $('div [id=headimg]').each(function () {
                            $(this).attr('src', targetPath);
                        });
                        setTimeout(function () {
                            Update_Page('index.html', false, false);
                        }, 3000);
                    }
                    else if (data.message == 'error') {
                        //登录失败
                        mdui.snackbar({
                            message: data.why,
                            position: 'bottom',
                        });
                    }
                    else {
                        //内部错误
                        alert('内部错误')
                    };
                },
                error: function () {
                    mdui.snackbar({
                        message: "服务器走丢啦，客官一会再来~(〃'▽'〃)",
                        position: 'bottom',
                    });
                },
            });
        };
    }
    else {  //未填写完整
        mdui.snackbar({
            message: '请完整填写登录信息哟(￣▽￣)~*',
            position: 'bottom',
        });
    };
};