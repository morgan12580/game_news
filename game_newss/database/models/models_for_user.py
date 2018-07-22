#!/user/bin/env python3
# -*- coding:utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from game_newss.database.exts import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telephone = db.Column(db.String(11), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # 优化密码 使密码保存在数据库中显示的是加密后的密码
    def __init__(self, *args, **kwargs):
        telephone = kwargs.get('telephone')
        username = kwargs.get('username')
        password = kwargs.get('password')

        self.telephone = telephone
        self.username = username
        self.password = generate_password_hash(password)

    #  判断密码是否相同
    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)
        return result


# 提问
class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # now()表示服务器第一次运行的时间
    # now表示没创建一个模型的时候，获取当前的时间
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref=db.backref('questions'))


# 评论
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    create_time = db.Column(db.DateTime, default=datetime.now)

    question = db.relationship('Question', backref=db.backref('answers', order_by=id.desc()))
    author = db.relationship('User', backref=db.backref('answers'))
