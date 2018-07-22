#!/user/bin/env python3
# -*- coding:utf-8 -*-
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from game_news.severs import app
from game_news.user.exts import db
from game_news.user.models_for_user import User, Question, Answer
manager = Manager(app)

# 绑定app和db
migrate = Migrate(app, db)

# 加迁移脚本的命令到manager中

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
