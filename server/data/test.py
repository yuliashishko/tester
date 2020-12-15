import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase

test_question = sqlalchemy.Table('test_question', SqlAlchemyBase.metadata,
                                 sqlalchemy.Column('id_test', sqlalchemy.Integer,
                                                   sqlalchemy.ForeignKey('test.id_test')),
                                 sqlalchemy.Column('id_question', sqlalchemy.Integer,
                                                   sqlalchemy.ForeignKey('question.id_question'))
                                 )


class Test(SqlAlchemyBase):
    __tablename__ = 'test'
    id_test = sqlalchemy.Column(sqlalchemy.Integer,
                                primary_key=True, autoincrement=True)
    max_mark = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    duration = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    questions = orm.relation("Question",
                             secondary="test_question")
    exams = orm.relation("Exam", back_populates='test')
