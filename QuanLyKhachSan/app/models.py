from sqlalchemy import Column, Integer, Boolean, Float, String, Text, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from app import db, app
from enum import Enum as UserEnum
from flask_login import UserMixin
from datetime import datetime


class UserRoleEnum(UserEnum):
    USER = 1
    ADMIN = 2


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class Category(BaseModel):
    __tablename__ = 'LoaiPhong'

    name = Column(String(50), nullable=False)
    Rooms = relationship('Room', backref='category', lazy=False)

    def __str__(self):
        return self.name


class Room(BaseModel):
    __tablename__ = 'Phong'

    name = Column(String(50), nullable=False)
    price = Column(Float, default=0)
    image = Column(String(255))
    active = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    receipt_details = relationship('ReceiptDetails', backref='room', lazy=True)
    comments = relationship('Comment', backref='room', lazy=True)

    def __str__(self):
        return self.name

class User(BaseModel, UserMixin):
    __tablename__ = 'NguoiDung'

    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(255))
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)
    active = Column(Boolean, default=True)
    receipts = relationship('Receipt', backref='user', lazy=True)
    comments = relationship('Comment', backref='user', lazy=True)

    def __str__(self):
        return self.name


class Receipt(BaseModel):
    __tablename__ = 'HoaDon'

    name = Column(String(50))
    CCCD = Column(String(12))
    created_date = Column(DateTime, default=datetime.now())
    end_date = Column(DateTime)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetails', backref='receipt', lazy=True)


class ReceiptDetails(BaseModel):
    __tablename__ = 'HoaDonChiTiet'

    price = Column(Float, default=0)
    Room_id = Column(Integer, ForeignKey(Room.id), nullable=False)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)


class Comment(BaseModel):
    __tablename__ = 'BinhLuan'

    content = Column(String(255), nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)

    def __str__(self):
        return self.content


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # c1 = Category(name='Phòng đơn')
        # c2 = Category(name = 'Phòng đôi')
        #
        # db.session.add(c1)
        # db.session.add(c2)
        #
        # db.session.commit()

        # p1 = Room(name='101', price=100000,image='https://images.pexels.com/photos/3209035/pexels-photo-3209035.jpeg',category_id=1)
        # p2 = Room(name='102', price=100000,image='https://images.pexels.com/photos/271655/pexels-photo-271655.jpeg',category_id=1)
        # p3 = Room(name='103', price=200000,image='https://images.pexels.com/photos/1329711/pexels-photo-1329711.jpeg', category_id=2)
        # p4 = Room(name='104', price=200000,image='https://images.pexels.com/photos/262048/pexels-photo-262048.jpeg', category_id=2)
        # p5 = Room(name='105', price=100000,image='https://images.pexels.com/photos/271618/pexels-photo-271618.jpeg', category_id=1)
        # p6 = Room(name='106', price=200000,image='https://images.pexels.com/photos/2631746/pexels-photo-2631746.jpeg',category_id=2)
        # p7 = Room(name='107', price=100000,image='https://images.pexels.com/photos/1571450/pexels-photo-1571450.jpeg', category_id=1)
        # p8 = Room(name='108', price=200000,image='https://images.pexels.com/photos/2416932/pexels-photo-2416932.jpeg',category_id=2)
        #
        # db.session.add(p1)
        # db.session.add(p2)
        # db.session.add(p3)
        # db.session.add(p4)
        # db.session.add(p5)
        # db.session.add(p6)
        # db.session.add(p7)
        # db.session.add(p8)
        #
        # db.session.commit()

        # import hashlib
        #
        # password = str(hashlib.md5("123456".strip().encode('utf-8')).hexdigest())
        # u1 = User(name='admin', username='admin', password=password,
        #           avatar='https://res.cloudinary.com/dfhexl1gh/image/upload/v1667869523/cld-sample-2.jpg',
        #           user_role=UserRoleEnum.ADMIN)
        #
        # db.session.add(u1)
        # db.session.commit()