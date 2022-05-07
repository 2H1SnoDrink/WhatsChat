# -*- coding: utf-8 -*-
import hashlib

db = {}

def get_md5(password):
    md5 = hashlib.md5()
    # 此处密码hash加密处理
    md5.update(password.encode('utf-8'))
    return md5.hexdigest()


def register(username, password):
    pwd = db.get(username, -1)
    if pwd == -1:
        db[username] = get_md5(username + password + '123456')
        print('注册成功！')
        print('user:%s' % username)
        print('md5:%s' % db[username])
    else:
        print('用户已经存在！')


def login(username, password):
    pwd = db.get(username, -1)  # db.get()方法是获取value,若不存在返回-1
    if pwd == -1:
        print('用户不存在！')
    elif get_md5(username + password + '123456') != pwd:
        print('用户名或密码不正确！')
    else:
        print('欢迎您，%s' % username)


print('开始注册！')
user = input('user:')
password = input('password:')
register(user, password)
print('开始登陆！')
user = input('user:')
password = input('password:')
login(user, password)