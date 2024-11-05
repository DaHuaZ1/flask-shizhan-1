from functools import wraps
from flask import session, redirect, url_for, g


def login_required(func):
    # 保留func的信息
    @wraps(func)
    # *args, **kwargs: 用来接收任意数量的参数， *args: 用来接收位置参数， **kwargs: 用来接收关键字参数
    def inner(*args, **kwargs):
        if g.user:
            return func(*args, **kwargs)
        else:
            return redirect(url_for("auth.login"))

    return inner

# 演示示例
# 只有登录用户才能访问question_public这个视图函数
# @login_required
# def question_public(question_id):
#     pass

# 上面的代码等价于下面的代码
# login_required(question_public)(question_id)
