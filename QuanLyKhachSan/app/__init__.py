from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babelex import Babel
import cloudinary

app = Flask(__name__)
app.secret_key = '12#^&*+_%&*)(*(&(*^&^$%$#((*65t87676'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/data1?charset=utf8mb4' % quote('Admin@123')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['MY_PAY'] = 'pay'

db = SQLAlchemy(app=app)
login = LoginManager(app=app)
babel = Babel(app=app)
cloudinary.config(cloud_name='dfhexl1gh', api_key='195159349819916', api_secret='zAN8Lucg7XQ5Wl8KgBoUQKZcUxs')


@babel.localeselector
def load_locale():
    return 'vi'
