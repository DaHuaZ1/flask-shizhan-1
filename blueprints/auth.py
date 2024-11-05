import random
from models import EmailCaptchaModel, UserModel
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from exts import mail, db
from flask_mail import Message
import string
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

# /auth, 添加url前缀，访问的时候就是 /auth/login
bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print("邮箱不存在!")
                return redirect(url_for("auth.login"))
            if check_password_hash(user.password, password):
                # cookie:
                # cookie中不适合存储太多的数据，只适合存储一些小数据
                # cookie一般用来存放登录授权的东西
                # flask中的session，是经过加密后存储在cookie中的
                session["user_id"] = user.id
                return redirect("/")
            else:
                print("密码错误!")
                return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.login"))


# GET: 获取数据从服务器
# POST: 提交数据到服务器
@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        # 验证用户提交的邮箱和验证码是否对应且正确
        # 表单验证： flask-wtf: wtforms
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))  # 生成密码的hash加密
            db.session.add(user)
            db.session.commit()
            # return redirect("/auth/login")
            return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.register"))


@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# bp.route: 如果没有制定methods，默认是GET请求
@bp.route("/captcha/email")
def get_email_captcha():
    # /captcha/email?email=xxx
    # /captcha/email/<email>
    email = request.args.get("email")
    # 4/6位随机验证码: 随机数组、字母、数组和字母的组合
    # string.digits * 4: 0123456789012345678901234567890123456789
    source = string.digits * 4
    captcha = random.sample(source, 4)
    captcha = "".join(captcha)
    # 此处为I/O操作: Input/Output, 耗时长,（需要异步操作）
    message = Message(subject="快问快答注册验证码", recipients=[email], body=f"您的验证码是：{captcha}")
    mail.send(message)
    # 服务器端保存验证码
    # 1.memcached: 存在内存中，速度快，但是重启就没有了，没有同步机制
    # 2.redis: 存在硬盘中，速度慢，但是重启还在，有同步机制
    # 3.用数据库的方式存储验证码，速度慢，小体量的网站可以使用
    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    # RESTful API: 一种风格、一种规范, 统一一种格式
    # {code: 200/400/500, message: "xxx", data: {}}
    return jsonify({"code": 200, "message": "", "data": None})


@bp.route('/mail/test')
def mailtest():
    message = Message(subject="邮件主题", recipients=["1476115724@qq.com"], body="这是一条测试邮件")
    mail.send(message)
    return "邮件发送成功"
