#!/user/bin/env python3
# -*- coding:utf-8 -*-
from flask import Flask, session, g

from game_newss.config import config
from game_newss.views import bp_home

from game_newss.database.exts import db
from game_newss.database.models.models_for_user import User

# 初始化一个app
app = Flask(__name__)
# 初始化配置文件
app.config.from_object(config)
#
app.register_blueprint(bp_home)
# 分开Models解决循环引用的问题
db.init_app(app)


@app.before_request
def my_before_request():
    """
    钩子函数
    使用g对象 优化 重复部分代码
    :return:
    """
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user


@app.context_processor
def my_context_processor():
    """
    before_request -> 视图函数 ——>context_processor
    :return:
    """
    if hasattr(g, 'user'):
        return {'user': g.user}
    return {}


if __name__ == '__main__':
    app.run(debug=True)
