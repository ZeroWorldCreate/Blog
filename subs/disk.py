# coding=UTF-8
# 微型Server服务器，存储中转站数据

# 库引入
import socket
import threading
import json

# 变量声明

# Tokens
Reg_Tokens = {}         # sha256字符
Email_Tokens = {}       # 简单6位16进制


# 功能类定义

# Handlers for Tokens
class TokenHandlers():
    def __init__(self):
        pass

    # Token验证类
    def addToken(self, dict_Token):
        # 添加新的Token
        Reg_Tokens.update(dict_Token)
        # print(Reg_Tokens)
    def searchToken(self, username, U_Token):
        # 搜索是否存在需求Token
        # print(1)
        seh = Reg_Tokens.get(username, False)
        # print(seh)
        if (seh != False):
            if (seh == U_Token):
                return True
            elif (seh != U_Token):
                return False
            else:
                return False
        elif (seh == False):
            return False
        else:
            return False

    def delToken(self, username):
        # 删除已验证Token
        state = Reg_Tokens.pop(username, False)
        if (state == False):
            return False
        elif (state != False):
            return True

hToken = TokenHandlers()


# 构造服务器

# 客户数据处理函数声明

# 深入交流
def dataHandler(need, sk):
    if (need == 1):
        # GET
        bind_token = sk.recv(1024)
        bind_token = json.loads(bind_token.decode('utf-8'))
        # print(bind_token)
        hToken.addToken(bind_token)
    elif (need == 2):
        # POST
        username = sk.recv(1024)
        username = username.decode('utf-8')
        sk.send(' '.encode('utf-8')) # 发送空格告知可以继续发送数据
        U_Token = sk.recv(2048)
        U_Token = U_Token.decode('utf-8')
        state = hToken.searchToken(username, U_Token)
        if (state == True):
            #可以注册（验证成功）
            sk.send('True'.encode('utf-8'))
            state = hToken.delToken(username)
            # 若返回False，再次删除，避免硬错误
            if (state == False):
                hToken.delToken(username)
        elif (state == False):
            #不能注册（验证失败）
            sk.send('False'.encode('utf-8'))
    elif (need == 3):
        # EMAIL
        pass
    else:
        # ERROR
        print('ERROR(if_dataHandler)')


# 初次握手
def clientData(sk, addr):
    # 验证类型
    sk.send('what'.encode('utf-8'))
    what = sk.recv(1024)
    what = what.decode('utf-8')
    if (what == 'GET'):
        # print('Get!')
        dataHandler(1, sk)
    elif (what == 'POST'):
        # print('Post')
        dataHandler(2, sk)
    elif (what == 'EMAIL'):
        # print('Email')
        dataHandler(3, sk)
    
    
    
    else:
        print('ERROR(if_clientData)')
        print(what)


# 构造Socket实例
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 包装实例
s.bind(('127.0.0.1', 32648))
# 启用监听
s.listen(5)
print('Disk System is ready')
while True:
    # 验证身份（后续按需求决定）
    sock, addr = s.accept()
    t = threading.Thread(target=clientData(sock, addr))
    t.start()



