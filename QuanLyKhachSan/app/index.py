from flask import session
from app import app, dao, login, controllers
# from app import utils
from app import admin


app.add_url_rule('/', 'index', controllers.index)
app.add_url_rule('/rooms/<int:room_id>', 'room-detail', controllers.room_detail)
app.add_url_rule('/register', 'register', controllers.register, methods=['get', 'post'])
app.add_url_rule('/login', 'login-user', controllers.login_my_user, methods=['get', 'post'])
app.add_url_rule('/logout', 'logout', controllers.logout_my_user)
app.add_url_rule('/login-admin', 'login-admin', controllers.login_admin, methods=['post'])
app.add_url_rule('/rooms/<room_id>/comments', 'comments', controllers.comments)
app.add_url_rule('/rooms/<room_id>/comments', 'comment-add', controllers.add_comment, methods=['post'])
app.add_url_rule('/category','cate', controllers.cate_room)
app.add_url_rule('/form','form', controllers.form)
app.add_url_rule('/rent','rent', controllers.rent)
app.add_url_rule('/pay','pay', controllers.pay)

@login.user_loader
def user_load(user_id):
    return dao.get_user_by_id(user_id)

if __name__ == '__main__':
    app.run(debug=True)

