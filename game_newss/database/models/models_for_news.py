#!/user/bin/env python3
# -*- coding:utf-8 -*-
from sqlalchemy import Column, Integer, String, create_engine, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

DB_URI = 'mysql+mysqldb://root:newpass@localhost:3306/youxi_demo?charset=utf8'

engine = create_engine(DB_URI)
Base = declarative_base(engine)
session_db = sessionmaker(engine)()


# 热门游戏
class Mod_game(Base):
    __tablename__ = 'mode_game'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    url = Column(Text)
    clss = Column(String(200))

    @classmethod
    def save_with_item(cls, item):
        mod_game = Mod_game()
        mod_game.name = item.get('name', '')
        mod_game.url = item.get('url', '')
        mod_game.clss = item.get('clss', '')
        session_db.add(mod_game)
        session_db.commit()
        return mod_game


# 轮播图片
class Images (Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True, autoincrement=True)
    image_url = Column(Text)
    image_alt = Column(String(100), nullable=False)
    new_url = Column(Text)

    @classmethod
    def save_with_item(cls, item):
        images = Images()
        images.image_url = item.get('image_url', '')
        images.image_alt = item.get('image_alt', '')
        images.new_url = item.get('new_url', '')
        session_db.add(images)
        session_db.commit()
        return images


# 当前热闻
class Hot_news(Base):
    __tablename__ = 'hot_news'
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(200), nullable=False)
    url = Column(Text)
    data = Column(String(200), nullable=False)

    @classmethod
    def save_with_item(cls, item):
        hot_newms = Hot_news()
        hot_newms.content = item.get('content', '')
        hot_newms.url = item.get('url', '')
        hot_newms.data = item.get('data', '')
        session_db.add(hot_newms)
        session_db.commit()
        return hot_newms


# 今日新闻
class Today_news(Base):
    __tablename__ = 'today_news'
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(200), nullable=False)
    image = Column(Text)
    author = Column(String(20), nullable=False)
    content = Column(Text)

    @classmethod
    def save_with_item(cls, item):
        today_news = Today_news()
        today_news.text = item.get('news_text', '')
        today_news.image = item.get('news_image', '')
        today_news.author = item.get('news_author', '')
        today_news.content = item.get('content', '')
        session_db.add(today_news)
        session_db.commit()
        return today_news


# 企鹅电竞的视频
class QieVideo(Base):
    __tablename__ = 'qie_video'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    picture = Column(Text, nullable=False)
    url = Column(Text, nullable=False)

    @classmethod
    def save_with_item(cls, item):
        qie_video = QieVideo()
        qie_video.name = item.get('video_name', '')
        qie_video.picture = item.get('video_picture', '')
        qie_video.url = item.get('video_url', '')
        session_db.add(qie_video)
        session_db.commit()
        return qie_video


# 厂商新闻
class FirmNews(Base):
    __tablename__ = 'firm_news'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50))
    url = Column(Text)

    @classmethod
    def save_with_item(cls, item):
        firm_news = FirmNews()
        firm_news.title = item.get('firm_news_title', '')
        firm_news.url = item.get('firm_news_url', '')
        session_db.add(firm_news)
        session_db.commit()
        return firm_news


# 置顶的第一个视频信息
class FirstVideo(Base):
    __tablename__ = 'first_video'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(20))
    photo = Column(Text)
    url = Column(Text)
    author = Column(String(20))

    @classmethod
    def save_with_item(cls, item):
        first_video = FirstVideo()
        first_video.title = item.get('video_title', '')
        first_video.photo = item.get('video_photo', '')
        first_video.url = item.get('video_url', '')
        first_video.author = item.get('video_author', '')
        session_db.add(first_video)
        session_db.commit()
        return first_video


# 视频
class GameVideo(Base):
    __tablename__ = 'game_video'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50))
    photo = Column(Text)
    url = Column(Text)
    author = Column(String(20))
    index = Column(Text)
    number = Column(String(20))

    @classmethod
    def save_with_item(cls, item):
        game_video = GameVideo()
        game_video.title = item.get('video_title', '')
        game_video.photo = item.get('video_photo', '')
        game_video.url = item.get('video_url', '')
        game_video.author = item.get('video_author', '')
        game_video.index = item.get('author_index', '')
        game_video.number = item.get('author_number', '')
        session_db.add(game_video)
        session_db.commit()
        return game_video


# 当前火热主播主页
class ModPerson(Base):
    __tablename__ = 'mod_person'
    id = Column(Integer, primary_key=True, autoincrement=True)
    photo = Column(Text)
    name = Column(String(20))
    url = Column(Text)

    @classmethod
    def save_with_item(cls, item):
        modperson = ModPerson()
        modperson.photo = item.get('photo', '')
        modperson.name = item.get('name', '')
        modperson.url = item.get('url', '')
        session_db.add(modperson)
        session_db.commit()
        return modperson


# 当前界面最热手游信息,客户端，网游，单机/主机游戏，专区资讯，
class ModALLGame(Base):
    __tablename__ = 'mode_phone'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100))
    create_time = Column(String(50))
    content = Column(Text)

    @classmethod
    def save_with_item(cls, item):
        phone = ModALLGame()
        phone.title = item.get('title', ' ')
        phone.create_time = item.get('create_time', ' ')
        phone.content = item.get('content', ' ')
        session_db.add(phone)
        session_db.commit()
        return phone


# 近期测试游戏
class RecentGame(Base):
    __tablename__ = 'recent_game'
    id = Column(Integer, primary_key=True, autoincrement=True)
    test_time = Column(String(20))
    game_name = Column(String(20))
    test_style = Column(String(10))
    download_url = Column(Text)

    @classmethod
    def save_with_item(cls, item):
        recent = RecentGame()
        recent.test_time = item.get('test_time', ' ')
        recent.game_name = item.get('game_name', ' ')
        recent.test_style = item.get('test_style', ' ')
        recent.download_url = item.get('download_url', ' ')
        session_db.add(recent)
        session_db.commit()
        return recent


# 游戏排行
class HotGameRank(Base):
    __tablename__ = 'game_rank'
    id = Column(Integer, primary_key=True, autoincrement=True)
    rank = Column(String(20))
    game_name = Column(String(20))
    number = Column(String(50))
    url = Column(Text)

    @classmethod
    def save_with_item(cls, item):
        game_rank = HotGameRank()
        game_rank.rank = item.get('rank', ' ')
        game_rank.game_name = item.get('game_name', ' ')
        game_rank.number = item.get('number', ' ')
        game_rank.url = item.get('url', '')
        session_db.add(game_rank)
        session_db.commit()
        return game_rank


# **********************************************************************
# 网易新闻
class WangYiNews(Base):
    __tablename__ = 'WY_news'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100))
    time = Column(String(20))
    remark = Column(Text)
    content_character = Column(Text)
    content_photo = Column(Text)

    @classmethod
    def save_with_item(cls, item):
        wynews = WangYiNews()
        wynews.title = item.get('title', ' ')
        wynews.time = item.get('time', '')
        wynews.remark = item.get('remark', '')
        wynews.content_character = item.get('content_character', '')
        wynews.content_photo = item.get('content_photo', '')
        session_db.add(wynews)
        session_db.commit()
        return wynews


Base.metadata.create_all()


# **********************************************************************
# 用户
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    telephone = Column(String(11), nullable=False)
    username = Column(String(20), nullable=False)
    password = Column(String(20), nullable=False)

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

    @classmethod
    def save_with_item(cls, item):
        user = User()
        user.telephone = item.get('telephone')
        user.username = item.get('username')
        user.password = item.get('password')
        session_db.add(user)
        session_db.commit
        return user
