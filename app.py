from flask import Flask, session, g
import config
from exts import db, mail
from models import UserModel
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from flask_migrate import Migrate

app = Flask(__name__)
# 绑定配置文件
app.config.from_object(config)

# init_app: 先创建再绑定
db.init_app(app)
mail.init_app(app)

migrate = Migrate(app, db)

# blueprints: 用来做模块化开发
app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)


# 钩子函数: 在请求之前或之后执行的函数，突然插入进来，先执行钩子函数，再执行视图函数
# before_request/ before_first_request/ after_request
# hook
@app.before_request
def my_before_request():
    user_id = session.get("user_id")
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g, "user", user)
    else:
        # g.user = None以免报错
        setattr(g, "user", None)


# 上下文处理器: 用来给模板引擎传递数据
@app.context_processor
def my_context_processor():
    return {"user": g.user}


if __name__ == '__main__':
    app.run()
