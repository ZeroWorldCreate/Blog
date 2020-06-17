# coding=UTF-8
# POST请求接收
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import socket
import data
from hashlib import sha256
from tornado.options import define, options
from os import path, mkdir
from shutil import copyfile


# 绑定地址
define('port', default=3000, type=int, help='Server Port')
Disk_addr = ('127.0.0.1', 32648)

# 数据库初始化
db, cursor = data._init()

hUser = data.C_user()


# 连接disk
def connectDisk(addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(addr)
    state = s.recv(1024)
    state = state.decode('utf-8')
    # print(state)
    if (state == 'what'):
        s.send('POST'.encode('utf-8'))
        return s


# seahToken && delToken
def s_dToken(username, U_Token):
    s = connectDisk(Disk_addr)
    s.send(username.encode('utf-8'))
    s.recv(1024)    #等待disk响应
    s.send(U_Token.encode('utf-8'))
    state = s.recv(1024)
    return state

# 新建以用户名命名的文件目录集
def mkUserDir(username):
    parentDir = path.dirname(path.dirname(__file__))# 父目录
    # 创建相对父目录（相对于用户配置文件）
    userDir = parentDir + "/users/" + username
    indexDir = parentDir + '/index/user/'
    mkdir(userDir)
    # 创建其余配置文件目录
    mkdir((userDir + '/headimg/'))
    copyfile((indexDir + '/headimg/headimg.jpg'), (userDir + '/headimg/headimg.jpg'))# 默认头像
    

# 定义继承类
class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST')


# POST请求
class RegisterHandler(BaseHandler):   # 注册
    def post(self):
        U_Token = self.get_argument('Token')
        username = self.get_argument('username')
        pwd = self.get_argument('pwd')
        Email = self.get_argument('Email')
        # print('getok')
        state = s_dToken(username, U_Token)
        state = state.decode('utf-8')
        # print(state)
        if (pwd != None):
            if (state == 'True'):
                # 验证成功，开始邮箱验证
                
                # 哈希处理密码
                pwd = sha256(pwd.encode('utf-8')).hexdigest()
                # print(username, pwd, Email, U_Token)
                w_state = hUser.main(db, cursor, username, pwd, Email, 1)
                if (w_state == True):
                    # 写入成功
                    # 新建以用户名命名的文件目录
                    mkUserDir(username)
                    U_Token, username, pwd, Email, state, w_state = None, None, None, None, None, None
                    self.finish({'message':'ok'})
                else:
                    # 写入失败，内部错误
                    U_Token, username, pwd, Email, state, w_state = None, None, None, None, None, None
                    self.finish({'message':'error','why':'内部错误'})
            elif (state == 'False'):
                # 验证失败，丢弃数据
                U_Token, username, pwd, Email, state = None, None, None, None, None
                self.finish({'message':'error','why':'Token校验错误'})
            else:
                U_Token, username, pwd, Email, state = None, None, None, None, None
                self.finish({'message':'error','why':'内部错误'})
        else:
            return False

class LoginHandler(BaseHandler):   # 登录
    def post(self):
        username = self.get_argument('username')
        pwd = self.get_argument('pwd')  #此处传递密码为sha256
        how = self.get_argument('type')
        # print(username, pwd, how)
        if (username, pwd, how != None or username, pwd, how != ''):
            # 二次判断，是否为空（json第一次判断）
            if (how == 'Email'):
                # 邮箱模式
                state, S_username, why = hUser.main(db, cursor, username, pwd, username, 0.2)    # username与Email同用一个变量名，判断看need参数
                if (state == True):
                    # 查询成功，进行激活判断
                    username, pwd, how = None, None, None
                    self.finish({'message':'ok','user':S_username})
                else:
                    # 查询失败，拒绝登录
                    username, pwd, how = None, None, None
                    self.finish({'message':'error','why':why})
            elif (how == 'user'):
                # 用户名模式
                state, S_username, why = hUser.main(db, cursor, username, pwd, username, 0.1)    # username与Email同用一个变量名，判断看need参数
                if (state == True):
                    # 查询成功，进行激活判断
                    username, pwd, how = None, None, None
                    self.finish({'message':'ok','user':S_username})
                    username = None
                else:
                    # 查询失败，拒绝登录
                    username, pwd, how = None, None, None
                    self.finish({'message':'error','why':why})
            else:
                # 异常
                username, pwd, how = None, None, None
                self.finish({'message':'error','why':'内部错误'})
                return False

class indexHandler(BaseHandler):
    def post(self):
        pass

class SubBlogNoteHandler(BaseHandler):  # 发表博文
    def post(self):
        userToken = self.get_argument('userToken')
        blogNote = self.get_argument('blogNote')




# 主函数
def main():
    tornado.options.parse_command_line()
    # 定义APP
    app = tornado.web.Application(
        handlers=[
            (r'/register', RegisterHandler), 
            (r'/login', LoginHandler),
            (r'/', indexHandler),
            ]
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    print('POST System is ready')
    tornado.ioloop.IOLoop.instance().start()


main()
