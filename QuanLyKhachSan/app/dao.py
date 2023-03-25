from app.models import Category, Room, User, Receipt, ReceiptDetails, Comment
from app import db
from flask_login import current_user
from sqlalchemy import func
import hashlib

# loại phòng
def load_categories():
    return Category.query.all()

# Phòng
def load_room(category_id=None, kw=None):
    query = Room.query

    if category_id:
        query = query.filter(Room.category_id == category_id)

    if kw:
        query = query.filter(Room.name.contains(kw))

    return query.all()

# Phòng
def get_room_by_id(room_id):
    return Room.query.get(room_id)

# Người dùng
def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()

# đăng kí người dùng
def register(name, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name, username=username, password=password, avatar=avatar)
    db.session.add(u)
    db.session.commit()


def get_user_by_id(user_id):
    return User.query.get(user_id)


# thêm hóa đơn
def add_receipt(pay):
    if pay:
        r = Receipt(user=current_user)
        db.session.add(r)
        for c in pay.values():
            d = ReceiptDetails(price=c['price'],
                               receipt=r,
                               room_id=int(c['id']))
            db.session.add(d)
        try:
            db.session.commit()
        except:
            return False
        else:
            return True

# Đếm số lượng phòng
# def count_room_by_cate():
#     return db.session.query(Category.id, Category.name, func.count(Room.id))\
#                      .join(Room, Room.category_id.__eq__(Category.id), isouter=True)\
#                      .group_by(Category.id).all()

# bình luận
def load_comments_by_room(room_id):
    return Comment.query.filter(Comment.room_id.__eq__(room_id)).order_by(-Comment.id).all()

# thêm bình luận cho phòng
def add_comment(room_id, content):
    c = Comment(content=content, room_id=room_id, user=current_user)
    db.session.add(c)
    db.session.commit()

    return c

