# coding=UTF-8
# 敏感操作Token验证

import random
from hashlib import sha256

# 验证集合
class Verify():
    def __init__(self):
        super().__init__()

    def GetSubToken(self):          # 生成注册用Token
        num = random.randint(0, 100)
        Token = sha256(str(num).encode('utf-8')).hexdigest()
        return Token

    def EmailCheckToken(self):      # 生成邮件激活Token
        Token = []
        O_Token = ''
        i = 1
        bit = 6       # 验证码位数
        while i <= bit:     # 生成验证码数组
            num = str(random.randint(0, 9))
            lower = chr(random.randint(97, 122))  # 小写字母a~z
            upper = chr(random.randint(65, 90))  # 大写字母A~Z
            output = random.choice([num, lower, upper])
            Token.append(output)
            i += 1
        for i in Token:     # 转换为验证码字符串
            O_Token += str(i)
        # print(O_Token)
        return O_Token