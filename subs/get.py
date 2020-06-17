# coding=UTF-8
# GET请求接收

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import socket
import json
import data
from tokens import Verify
from tornado.options import define, options


# 绑定地址
define('port', default=2000, type=int, help='Server Port')
Disk_addr = ('127.0.0.1', 32648)

# 数据库初始化
db, cursor = data._init()

verify = Verify()


# 连接disk
def connectDisk(addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(addr)
    state = s.recv(1024)
    state = state.decode('utf-8')
    # print(state)
    if (state == 'what'):
        s.send('GET'.encode('utf-8'))
        return s


# getToken && saveToken
def g_sToken(username):
    s = connectDisk(Disk_addr)
    token = verify.GetSubToken()
    bind_token = {username:token}
    s.send(json.dumps(bind_token).encode('utf-8'))
    #print(bind_token)
    return token


# 定义继承类
class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET')

# GET请求
class CheckHandler(BaseHandler):
    def get(self):
        checkUsername = self.get_argument('username', None)
        # print(checkUsername)
        state = data.C_user.main(self, db, cursor, checkUsername, '', '', 2)
        if (state == True):
            self.finish({'message': 'error'})
        elif (state == False):
            self.finish({'message': 'ok', 'token': g_sToken(checkUsername)})
        else:
            self.finish({'message': 'I_error'})
        state = None


class newNote(BaseHandler):
    def get(self):
        pass


# 主函数
def main():
    tornado.options.parse_command_line()
    # 定义APP
    app = tornado.web.Application(
        handlers=[
            (r'/check', CheckHandler),
            (r'/newNote', newNote)
        ]
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    print('GET System is ready')
    tornado.ioloop.IOLoop.instance().start()


main()
