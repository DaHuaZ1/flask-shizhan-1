from flask import Blueprint, request, render_template, g, redirect, url_for
from .forms import QuestionForm, AnswerForm
from models import QuestionModel, AnswerModel
from exts import db
from decorators import login_required

# 此项目中问答页面是首页，所以url_prefix设置为"/"
bp = Blueprint("qa", __name__, url_prefix="/")


# http://127.0.0.1:5000
@bp.route("/")
def index():
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()

    return render_template("index.html", questions=questions)


@bp.route("/qa/public", methods=["GET", "POST"])
@login_required
def question_public():
    # if not g.user:
    #     return redirect(url_for("auth.login"))
    # 使用装饰器login_required代替上面的代码

    if request.method == "GET":
        return render_template("public_question.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            # todo: 跳转到这篇问答的详情页
            return redirect("/")
        else:
            print(form.errors)
            return redirect(url_for("qa.question_public"))


@bp.route('/qa/detail/<qa_id>')
def qa_detail(qa_id):
    question = QuestionModel.query.get(qa_id)
    return render_template("detail.html", question=question)


# @bp.route('/answer/public', methods=["POST"])
@bp.post('/answer/public')  # 等同于上面的写法，只是更简洁
@login_required
def public_answer():
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        answer = AnswerModel(content=content, question_id=question_id, author_id=g.user.id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for("qa.qa_detail", qa_id=question_id))
    else:
        print(form.errors)
        return redirect(url_for("qa.qa_detail", qa_Id=request.form.get("question_id")))


@bp.route('/search')
@login_required
def search():
    # /search?q=xxx
    # /search/<q>
    # post, request.form
    q = request.args.get("q")
    questions = QuestionModel.query.filter(QuestionModel.title.contains(q) | QuestionModel.content.contains(q)).all()
    return render_template("index.html", questions=questions)

# url传参
# 邮件发送
# ajax
# orm与数据库
# jinja2模版
# cookie与session
# flask蓝图
# 搜索

