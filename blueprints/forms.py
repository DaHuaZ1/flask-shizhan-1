import wtforms
from wtforms.validators import Email, Length, EqualTo, InputRequired
from models import UserModel, EmailCaptchaModel
from exts import db


# Form: 主要就是用来验证前端提交的数据是否符合要求
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="请输入正确的邮箱格式")])
    captcha = wtforms.StringField(validators=[Length(4, 4, message="请输入正确格式的验证码")])
    username = wtforms.StringField(validators=[Length(3, 20, message="请输入正确格式的用户名")])
    password = wtforms.StringField(validators=[Length(6, 20, message="请输入正确格式的密码")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password", message="两次密码不一致")])

    # 自定义验证：
    # 1.验证邮箱是否已经被注册
    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError("邮箱已经被注册")

    # 2.验证验证码是否正确
    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        email_captcha = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        if not email_captcha:
            raise wtforms.ValidationError("邮箱或验证码错误")
        # else:
        #     # todo: 可以删掉email_captcha, 过期的验证码没有意义了
        #     email_captcha.used = True
        #     db.session.delete(email_captcha)
        #     db.session.commit()


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="请输入正确的邮箱格式")])
    password = wtforms.StringField(validators=[Length(6, 20, message="请输入正确格式的密码")])
    # remember = wtforms.StringField()  # 是否记住登录状态


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(3, 100, message="请输入正确格式的标题")])
    content = wtforms.StringField(validators=[Length(3, message="请输入正确格式的内容")])


class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[Length(3, message="请输入正确格式的内容")])
    question_id = wtforms.IntegerField(validators=[InputRequired(message="必须要传入问题id")])