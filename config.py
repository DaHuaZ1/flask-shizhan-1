
SECRET_KEY = "asdfgjhjkl;sdf"


# 数据库的配置信息
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'flask_shizhan1'
USERNAME = 'root'
PASSWORD = 'root'
DB_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4'
SQLALCHEMY_DATABASE_URI = DB_URI


# 邮箱配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_USE_SSL = True  # 加密开启
MAIL_PORT = 465
MAIL_USERNAME = '3231187585@qq.com'
MAIL_PASSWORD = 'gfjmbegxrfzadadf' # gfjmbegxrfzadadf
MAIL_DEFAULT_SENDER = '3231187585@qq.com'



















