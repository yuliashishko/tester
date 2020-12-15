import sqlalchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class People(SqlAlchemyBase, UserMixin):
    __tablename__ = 'people'

    id_people = sqlalchemy.Column(sqlalchemy.Integer,
                                  primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    group = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    username = sqlalchemy.Column(sqlalchemy.String,
                                 index=True, unique=True, nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    exams = orm.relation("Exam", back_populates='people')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
