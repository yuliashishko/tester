import datetime

from flask import Flask, render_template, request, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy.ext.declarative import DeclarativeMeta
from flask_cors import CORS
from werkzeug.security import generate_password_hash

from server.data import db_session
from server.data.answer import Answer
from server.data.exam import Exam
from server.data.people import People
from server.data.question import Question
from server.data.test import Test
import json

app = Flask(__name__)
CORS(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            return fields

        return json.JSONEncoder.default(self, obj)


@app.route('/people', methods=['GET'])
def people_get():
    session = db_session.create_session()
    response_object = {'status': 'success'}
    response_object['people'] = session.query(People).all()
    # return jsonify(response_object)
    return json.dumps(response_object, cls=AlchemyEncoder)


@app.route('/test', methods=['GET'])
def test_get():
    session = db_session.create_session()
    response_object = {'status': 'success'}
    response_object['test'] = session.query(Test).all()
    return json.dumps(response_object, cls=AlchemyEncoder)


@app.route('/questions', methods=['GET'])
def question_get():
    session = db_session.create_session()
    response_object = {'status': 'success'}
    response_object['questions'] = session.query(Question).all()
    return json.dumps(response_object, cls=AlchemyEncoder)


@app.route('/answer', methods=['GET'])
def answer_get():
    session = db_session.create_session()
    response_object = {'status': 'success'}
    response_object['answer'] = session.query(Answer).all()
    return json.dumps(response_object, cls=AlchemyEncoder)


@app.route('/exam', methods=['GET'])
def exam_get():
    session = db_session.create_session()
    response_object = {'status': 'success'}
    response_object['exam'] = session.query(Exam).all()
    return json.dumps(response_object, cls=AlchemyEncoder)


@app.route('/people', methods=['POST'])
def people_post():
    session = db_session.create_session()
    post_data = request.get_json()
    response_object = {'status': 'success'}
    peoples = session.query(People).filter(post_data.get('username') == People.username).all()
    if not peoples:
        people = People()
        people.group = post_data.get('group')
        people.name = post_data.get('name')
        people.username = post_data.get('username')
        people.set_password(post_data.get('password'))
        session.add(people)
        session.commit()
        response_object['message'] = 'New user created successfully'
    else:
        response_object['message'] = 'Such user already exist'
    return json.dumps(response_object, cls=AlchemyEncoder)


@app.route('/test', methods=['POST'])
def test_post():
    session = db_session.create_session()
    post_data = request.get_json()
    response_object = {'status': 'success'}
    tests = session.query(Test).filter(post_data.get('id_test') == Test.id_test).all()
    if not tests:
        test = Test(
            max_mark=post_data.get('max_mark'),
            duration=post_data.get('duration')
        )

        session.add(test)
        session.commit()
        response_object['message'] = 'New test created successfully'
    else:
        response_object['message'] = 'Such test already exist'
    return jsonify(response_object)


@app.route('/questions', methods=['POST'])
def question_post():
    session = db_session.create_session()
    post_data = request.get_json()
    response_object = {'status': 'success'}
    questions = session.query(Question).filter(post_data.get('id_question') == Question.id_question).all()
    if not questions:
        question = Question(
            max_mark=post_data.get('max_mark'),
            question_text=post_data.get('question_text'),
            answers=post_data.get('answers')
        )

        session.add(question)
        session.commit()
        response_object['message'] = 'New question created successfully'
    else:
        response_object['message'] = 'Such question already exist'
    return jsonify(response_object)


@app.route('/answer', methods=['POST'])
def answer_post():
    session = db_session.create_session()
    post_data = request.get_json()
    response_object = {'status': 'success'}
    answers = session.query(Answer).filter(post_data.get('id_answer') == Answer.id_answer).all()
    if not answers:
        answer = Answer(
            mark=post_data.get('mark'),
            answer_text=post_data.get('answer_text'),
            id_question=post_data.get('id_question')  # TODO: check id_test
        )

        session.add(answer)
        session.commit()
        response_object['message'] = 'New answer created successfully'
    else:
        response_object['message'] = 'Such answer already exist'
    return jsonify(response_object)


@app.route('/exam', methods=['POST'])
def exam_post():
    session = db_session.create_session()
    post_data = request.get_json()
    response_object = {'status': 'success'}
    exams = session.query(Exam).filter(post_data.get('id_exam') == Exam.id_exam).all()
    if not exams:
        exam = Exam(
            mark=post_data.get('mark'),
            date=post_data.get('date'),
            id_people=post_data.get('id_people'),
            answers=post_data.get('answers'),  # TODO:Check how to do an
            id_test=post_data.get('id_test')
        )
        session.add(exam)
        session.commit()
        response_object['message'] = 'New exam created successfully'
    else:
        response_object['message'] = 'Such exam already exist'
    return json.dumps(response_object, cls=AlchemyEncoder)


@app.route('/people/<id_people>', methods=['PUT'])
def people_update(id_people):
    session = db_session.create_session()
    response_object = {'status': 'success'}
    put_data = request.get_json()
    people = session.query(People).filter(People.id_people == id_people).first()
    if people:
        session.query(People).filter(People.id_people == id_people).update({
            'name': put_data['name'],
            'group': put_data['group'],
            'username': put_data['username'],
            'password': generate_password_hash(put_data['password'])
        })
        session.commit()
        response_object['message'] = 'User successfully updated'
    return jsonify(response_object)


@app.route('/test/<id_test>', methods=['PUT'])
def test_update(id_test):
    session = db_session.create_session()
    response_object = {'status': 'success'}
    put_data = request.get_json()
    test = session.query(Test).filter(Test.id_test == id_test).first()
    if test:
        test.update({
            'max_mark': put_data.get('max_mark'),
            'duration': put_data.get('duration'),
            'questions': put_data.get('questions')
        })
        session.commit()
        response_object['message'] = 'Test successfully updated'
    return jsonify(response_object)


@app.route('/questions/<id_question>', methods=['PUT'])
def question_update(id_question):
    session = db_session.create_session()
    response_object = {'status': 'success'}
    put_data = request.get_json()
    question = session.query(Question).filter(Question.id_question == id_question).first()
    if question:
        session.query(Question).filter(Question.id_question == id_question).update({
            'question_text': put_data.get('question_text'),
            'max_mark': put_data.get('max_mark'),
            'answers': put_data.get('answers')
        })
        session.commit()
        response_object['message'] = 'Question successfully updated'
    return jsonify(response_object)


@app.route('/answer/<id_answer>', methods=['PUT'])
def answer_update(id_answer):
    session = db_session.create_session()
    response_object = {'status': 'success'}
    put_data = request.get_json()
    answer = session.query(Answer).filter(Answer.id_answer == id_answer).first()
    if answer:
        answer.update({
            'answer_text': put_data.get('answer_text'),
            'mark': put_data.get('mark'),
            'id_question': put_data.get('id_question')
        })
        session.commit()
        response_object['message'] = 'Answer successfully updated'
    return jsonify(response_object)


@app.route('/exam/<id_exam>', methods=['PUT'])
def exam_update(id_exam):
    session = db_session.create_session()
    response_object = {'status': 'success'}
    put_data = request.get_json()
    exam = session.query(Exam).filter(Exam.id_exam == id_exam).first()
    if exam:
        exam.update({
            'id_test': put_data.get('id_test'),
            'mark': put_data.get('mark'),
            'answers': put_data.get('answers'),  # TODO
            'id_people': put_data.get('id_people'),
            'date': put_data.get('date')
        })

        session.commit()
        response_object['message'] = 'Exam successfully updated'
    return jsonify(response_object)


@app.route('/people/<id_people>', methods=['DELETE'])
def people_delete(id_people):
    session = db_session.create_session()
    response_object = {'status': 'success'}
    people = session.query(People).filter(People.id_people == id_people).first()
    if people:
        session.delete(people)
        session.commit()
        response_object['message'] = 'User successfully deleted'
    return jsonify(response_object)


@app.route('/test/<id_test>', methods=['DELETE'])
def test_delete(id_test):
    session = db_session.create_session()
    response_object = {'status': 'success'}
    test = session.query(Test).filter(Test.id_test == id_test).first()
    if test:
        session.delete(test)
        session.commit()
        response_object['message'] = 'Test successfully deleted'
    return jsonify(response_object)


@app.route('/questions/<id_question>', methods=['DELETE'])
def question_delete(id_question):
    session = db_session.create_session()
    response_object = {'status': 'success'}
    question = session.query(Question).filter(Question.id_question == id_question).first()
    if question:
        session.delete(question)
        session.commit()
        response_object['message'] = 'Question successfully deleted'
    return jsonify(response_object)


@app.route('/answer/<id_answer>', methods=['DELETE'])
def answer_delete(id_answer):
    session = db_session.create_session()
    response_object = {'status': 'success'}
    answer = session.query(Answer).filter(Answer.id_answer == id_answer).first()
    if answer:
        session.delete(answer)
        session.commit()
        response_object['message'] = 'User successfully deleted'
    return jsonify(response_object)


@app.route('/exam/<id_exam>', methods=['DELETE'])
def exam_delete(id_exam):
    session = db_session.create_session()
    response_object = {'status': 'success'}
    exam = session.query(Exam).filter(Exam.id_exam == id_exam).first()
    if exam:
        session.delete(exam)
        session.commit()
        response_object['message'] = 'User successfully deleted'
    return jsonify(response_object)


def main():
    db_session.global_init("db/tester.sqlite")
    app.run()


main()
# people = People(
#     name='name',
#     group='group',
#     id_people='id',
#     username='username',
#     password='password'
# )
# print(json.dumps(people, cls=AlchemyEncoder))
