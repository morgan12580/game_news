#!/user/bin/env python3
# -*- coding:utf-8 -*-
import os

from flask import Blueprint, render_template, request, redirect, url_for, session
from sqlalchemy import or_

from game_newss.config import BASE_DIR
from game_newss.dicorator.decorators import login_required
from game_newss.database.models.models_for_news import Mod_game, session_db, Images, WangYiNews, Hot_news, QieVideo, \
    Today_news, FirmNews, GameVideo, ModPerson, ModALLGame, RecentGame, HotGameRank

from game_newss.database.models.models_for_user import User, Question, Answer
from game_newss.database.exts import db


bp_home = Blueprint(__name__, __name__,
                    static_folder=os.path.join(BASE_DIR, 'static'),
                    template_folder=os.path.join(BASE_DIR, 'templates'),
                    url_prefix='/')


# 首页 ：腾讯游戏新闻
@bp_home.route('/')
def index():
    # 将数据库中所有信息查找出来
    mod_game = session_db.query(Mod_game).all()
    images = session_db.query(Images).all()
    hot_news = session_db.query(Hot_news).all()
    qie_videos = session_db.query(QieVideo).all()
    today_news = session_db.query(Today_news).all()
    firm_new = session_db.query(FirmNews).all()
    game_videos = session_db.query(GameVideo).all()
    persons = session_db.query(ModPerson).all()
    allnews = session_db.query(ModALLGame).all()
    games = session_db.query(RecentGame).all()
    other_game = session_db.query(HotGameRank).all()
    return render_template('index.html', mod_game=mod_game, images=images, hotnews=hot_news, qievideos=qie_videos,
                           todaynews=today_news, firmnews=firm_new, gamevideos=game_videos, persons=persons,
                           allnews=allnews, games=games, othergames=other_game, defult=1)


# 交流平台首页
@bp_home.route('/pt')
def pt():
    context = {
        'questions': Question.query.order_by('-create_time').all()
    }
    return render_template('pt.html', **context, defult=4)


# 网易游戏新闻
@bp_home.route('/wy')
def wy():
    context = {
        'news': session_db.query(WangYiNews).all()
    }
    return render_template('wyxw.html', **context, defult=2)


# 游戏交流平台
@bp_home.route('/question/', methods=['GET', 'POST'])
# 如果登陆了，可以发布问答  如果没有登陆 点击发布问答 跳到登陆界面
# 登陆限制装饰器
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html', defult=3)
    else:
        # 表单方式获取用户输入的内容并且存入数据库
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title, content=content)
        # user_id = session.get('user_id')
        # user = User.query.filter(User.id == user_id).first()
        question.author = g.user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('pt', defult=4))


# 登陆
@bp_home.route('/login/', methods=['GET', 'POST'])
def login():
    # 当get请求时，返回一个登录界面
    if request.method == 'GET':
        return render_template('login.html', defult=3)
    # 当post请求时，将用户名和密码与数据库中已注册的用户进行对比
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone).first()
        if user and user.check_password(password):
            # 设置session
            session['user_id'] = user.id
            # 设置过期时间 一个月
            session.pernament = True
            # 登录成功，自动跳转到首页
            return redirect(url_for('game_newss.views.home.index'))
        else:
            return u'手机号码或者密码错误，请检查后重新输入'


# 注册
@bp_home.route('/regist/', methods=['GET', 'POST'])
def regist():
    # 当get请求时，返回一个登录界面
    if request.method == 'GET':
        return render_template('regist.html',defult=3)
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # 手机号码验证，如果被注册了，就不能再注册
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return u'该手机号码已经被注册，请更换手机'
        else:
            # password1 2 相等
            if password1 != password2:
                return u'两次密码不想等，请核对后重新输入'
            else:
                # dic = {
                #     'telephone': telephone,
                #     'username': username,
                #     'password': password1
                # }
                # User.save_with_item(dic)
                user = User(telephone=telephone, username=username, password=password1)
                db.session.add(user)
                db.session.commit()
                # 如果注册成功，页面跳转到登陆界面
                return redirect(url_for('login'))


# 注销
@bp_home.route('/logoul/')
def logoul():
    # 清楚session
    session.clear()
    # 返回登录界面
    return redirect(url_for('game_newss.views.home.login'))


# 交流平台详情（点击首页内容标题）
@bp_home.route('/detail/<question_id>')
def detail_for_pt(question_id):
    question_demo = Question.query.filter(Question.id == question_id).first()
    # 统计 评论数
    count = Answer.query.filter(Answer.question_id == question_id).count()
    return render_template('detail_for_pt.html', question=question_demo, count=count,defult=4)


# 网易新闻详情
@bp_home.route('/detail2/<new_id>')
def detail_for_wy(new_id):
    new_demo = session_db.query(WangYiNews).filter(WangYiNews.id == new_id).first()
    return render_template('detail_for_wy.html', new=new_demo, defult=2)


# 腾讯今日新闻详情
@bp_home.route('/detail3/<new_id>')
def detail_for_tx(new_id):
    new_demo = session_db.query(Today_news).filter(Today_news.id == new_id).first()
    return render_template('detail_for_tx.html', new=new_demo, defult=1)


# 手游，端游，单机游戏等详情界面
@bp_home.route('/detail4/<new_id>')
def detail_for_news(new_id):
    new_demo = session_db.query(ModALLGame).filter(ModALLGame.id == new_id).first()
    return render_template('detail_for_news.html', new=new_demo,defult=1)


# 评论
@bp_home.route('/answer/', methods=['POST'])
@login_required
def add_answer():
    content = request.form.get('answer')
    question_id = request.form.get('question_id')
    answer = Answer(content=content)
    # user_id = session['user_id']
    # user = User.query.filter(User.id == user_id).first()
    answer.author = g.user
    question = Question.query.filter(Question.id == question_id).first()
    answer.question = question

    db.session.add(answer)
    db.session.commit()
    # 评论后 返回原标签
    return redirect(url_for('detail', question_id=question_id, ))


# 查找
@bp_home.route('/search/')
def search():
    q = request.args.get('q')
    questions = Question.query.filter(or_(Question.title.contains(q),
                                          Question.content.contains(q)))
    return render_template('pt.html', questions=questions, defult=4)
