import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Answer(SqlAlchemyBase):
    __tablename__ = 'answer'

    id_answer = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    mark = sqlalchemy.Column(sqlalchemy.Integer)
    answer_text = sqlalchemy.Column(sqlalchemy.String)

    id_test = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("test.id_test"))

    id_question = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("question.id_question"))
    question = orm.relation('Question')
