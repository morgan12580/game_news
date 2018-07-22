#!/user/bin/env python3
# -*- coding:utf-8 -*-

from functools import wraps
from flask import session, redirect, url_for


# 登陆限制的装饰器
def login_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('game_newss.views.home.login', defult=3))
    return wrapper
