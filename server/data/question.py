import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Question(SqlAlchemyBase):
    __tablename__ = 'question'
    id_question = sqlalchemy.Column(sqlalchemy.Integer,
                                    primary_key=True, autoincrement=True)
    max_mark = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    question_text = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    answers = orm.relation("Answer", back_populates='question')
