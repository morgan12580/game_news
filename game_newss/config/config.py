#!/user/bin/env python3
# -*- coding:utf-8 -*-

import os

SECRET_KEY = os.urandom(24)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DIALECT = 'mysql'
DRIVER = 'mysqldb'
USERNAME = 'root'
PASSWORD = 'newpass'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'youxi_demo'

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,
                                                                       DRIVER,
                                                                       USERNAME,
                                                                       PASSWORD,
                                                                       HOST,
                                                                       PORT,
                                                                       DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False


print(BASE_DIR)
