# coding=UTF-8
# 数据库操作

# 导入模块
import pymysql


# 初始化函数
def _init():

    # 连接数据库
    db = pymysql.connect(
        host='localhost',
        port=3306,
        user='Blog',
        passwd='20041123',
        db='alimo1029-blog',
        charset='utf8'
    )

    # 创建游标
    cursor = db.cursor()
    return db, cursor


class C_user():
    def __init__(self):
        super().__init__()

    def addUser(self, db, cursor, username, password, Email):
        # 添加新用户
        try:
            args = (username, password, Email)
            sql = "INSERT INTO users(username, password, Email) VALUES (%s,%s,%s)"
            # print(sql)
            cursor.execute(sql, args)
            db.commit()
            return True
        except:
            # 异常
            db.rollback()
            return False

    def main(self, db, cursor, username, password, Email, need):
        """need = 0.1代表登录模式（用户名）
           need = 0.2代表登录模式（邮箱）
           need = 1代表注册模式
           need = 2代表单纯查询
        """
        # 搜索数据库
        args = (username, password)
        L_sql_U = "SELECT username FROM users WHERE username = %s AND password = %s"
        L_sql_E = "SELECT username FROM users WHERE Email = %s AND password = %s"
        L_sql_A = "SELECT username FROM users WHERE username = %s AND password = %s AND isActivate = 1"
        R_sql = "SELECT username FROM users WHERE username = %s"
        S_sql = "SELECT username FROM users WHERE username = %s"
        # print(L_sql)
        if (need == 0.1):
            # 登录模式（用户名）
            cursor.execute(L_sql_U, args)
            sehData = cursor.fetchone()
            if (sehData != None):
                # 账号和密码组合获取成功
                # print('ok')
                # print(sehData)
                cursor.execute(L_sql_A, args)
                sehData = cursor.fetchone()
                if (sehData != None):
                    # 此账号已激活，成功登录
                    return True, sehData[0], None
                    sehData = None
                else:
                    return False, None, '账号未激活'
                    sehData = None
            else:
                # 获取不到，账号或密码错误
                # print('sorry')
                return False, None, '账号或密码错误'
        elif (need == 0.2):
            # 登录模式（邮箱）
            args = (Email, password)    # 特殊表单特殊声明
            cursor.execute(L_sql_E, args)
            sehData = cursor.fetchone()
            if (sehData != None):
                # 账号和密码组合获取成功
                # print('ok')
                # print(sehData)
                cursor.execute(L_sql_A, args)
                sehData = cursor.fetchone()
                if (sehData != None):
                    # 此账号已激活，成功登录
                    return True, sehData[0], None
                    sehData = None
                else:
                    return False, None, '账号未激活'
                    sehData = None
            else:
                # 获取不到，账号或密码错误
                # print('sorry')
                return False, None, '账号或密码错误'
        elif (need == 1):
            # 注册模式
            cursor.execute(R_sql, username)
            sehData = cursor.fetchone()
            if (sehData == None):
                # 无人使用，可以注册
                self.addUser(db, cursor, username, password, Email)
                #db.commit()
                return True
            else:
                # 有人使用，禁止注册
                sehData = None
                return False
        elif (need == 2):
            # 查询模式
            cursor.execute(S_sql, username)
            sehData = cursor.fetchone()
            db.commit()
            if (sehData != None):
                # 查有此人
                return True
            else:
                # 查无此人
                sehData = None
                return False
        else:
            return False

    def delUser(self, db, cursor, username):
        # 删除指定用户
        sql = "DELETE FROM users WHERE username = %s"
        try:
            cursor.execute(sql, username)
            db.commit()
            return True
        except:
            return False

# db, cursor = _init()
# print(C_user.addUser(db, cursor, 'limo1029', '20041123'))
# print(C_user.main(db, cursor, 'limo1029asd', '20041123', '1282160815@qq.com', 1))
# print(C_user.delUser(db, cursor, 'limo1029'))