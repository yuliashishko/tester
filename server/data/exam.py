import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase

reply = sqlalchemy.Table('reply', SqlAlchemyBase.metadata,
                         sqlalchemy.Column('id_exam', sqlalchemy.Integer,
                                           sqlalchemy.ForeignKey('exam.id_exam')),
                         sqlalchemy.Column('id_answer', sqlalchemy.Integer,
                                           sqlalchemy.ForeignKey('answer.id_answer'))
                         )


class Exam(SqlAlchemyBase):
    __tablename__ = 'exam'

    id_exam = sqlalchemy.Column(sqlalchemy.Integer,
                                primary_key=True, autoincrement=True)
    id_people = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey("people.id_people"))
    people = orm.relation('People')
    id_test = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("test.id_test"))
    test = orm.relation('Test')
    answers = orm.relation("Answer",
                           secondary="reply")
    mark = sqlalchemy.Column(sqlalchemy.Integer)
    date = sqlalchemy.Column(sqlalchemy.Date)
