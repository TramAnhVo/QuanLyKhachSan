from flask import render_template, request, redirect, jsonify,session
from app import app, dao
from flask_login import login_user, logout_user, login_required
import cloudinary.uploader
from app.decorators import annonymous_user
from app import utils


def index():
    return render_template('index.html')

def form():
    return render_template('form.html')

def rent():
    return render_template('rent.html')

# trang phòng chi tiết
def room_detail(room_id) :
    r = dao.get_room_by_id(room_id)
    return render_template('details.html', room = r)

def cate_room():
    cate_id = request.args.get('category_id')
    kw = request.args.get('keyword')
    rooms = dao.load_room(category_id=cate_id, kw=kw)
    return render_template('category.html', rooms = rooms)


# đăng kí người dùng
def register():
    err_msg = ''
    if request.method == 'POST':
        password = request.form['password']
        confirm = request.form['confirm']
        if password.__eq__(confirm):
            # upload cloudinary
            avatar=''
            if request.files:
                res = cloudinary.uploader.upload(request.files['avatar'])
                avatar = res['secure_url']

            # Lưu user
            try:
                dao.register(name=request.form['name'],
                             username=request.form['username'],
                             password=request.form['password'],
                             avatar=avatar)
            except:
                err_msg = 'Đã có lỗi xảy ra! Vui lòng đăng nhập lại!!!!!'
            else:
                return redirect('/login')
        else:
            err_msg = 'Mật khẩu không đúng!!!'

    return render_template('register.html', err_msg=err_msg)


@annonymous_user
def login_my_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)

            url_next = request.args.get('next')

            return redirect(url_next if url_next else '/')

    return render_template('login.html')


def logout_my_user():
    logout_user()
    return redirect('/login')


def login_admin():
    username = request.form['username']
    password = request.form['password']

    u = dao.auth_user(username=username, password=password)
    if u:
        login_user(user=u)

    return redirect('/admin')


@login_required
def pay():
    return render_template('pay.html')

# bình luận
def comments(room_id):
    data = []
    for c in dao.load_comments_by_room(room_id=room_id):
        data.append({
            'id': c.id,
            'content': c.content,
            'created_date': str(c.created_date),
            'user': {
                'name': c.user.name,
                'avatar': c.user.avatar
            }
        })

    return jsonify(data)


# thêm bình luận
def add_comment(room_id):
    try:
        c = dao.add_comment(room_id, request.json['content'])
    except:
        return jsonify({'status': 500})
    else:
        return jsonify({
            'status': 204,
            'comment': {
                'id': c.id,
                'content': c.content,
                'created_date': str(c.created_date),
                'user': {
                    'name': c.user.name,
                    'avatar': c.user.avatar
                }
            }
        })