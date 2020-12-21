import datetime
import time

import sqlalchemy
from flask import Flask, render_template, request, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy import func
from sqlalchemy.ext.declarative import DeclarativeMeta
from flask_cors import CORS
from werkzeug.security import generate_password_hash
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

import server
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
jwt = JWTManager(app)
from sqlalchemy.ext.declarative import DeclarativeMeta


def new_alchemy_encoder():
    _visited_objs = []

    class AlchemyEncoder(json.JSONEncoder):
        def default(self, obj):
            if type(obj) == datetime.date:
                return obj.isoformat()

            elif isinstance(obj.__class__, DeclarativeMeta):
                # don't re-visit self
                if obj in _visited_objs:
                    return None
                _visited_objs.append(obj)

                # an SQLAlchemy class
                fields = {}
                # for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata' and not callable()]:
                for field in dir(obj):
                    if not field.startswith('_') and field != 'metadata' and not callable(getattr(obj, field)):
                        fields[field] = obj.__getattribute__(field)

                # a json-encodable dict
                return fields


            return json.JSONEncoder.default(self, obj)

    return AlchemyEncoder


def nested_jsonifier(allowlist, blocklist):
    def jsonifiable(obj):
        try:
            json.dumps(obj)
            return True
        except TypeError as e:
            return False

    def in_list(type_field_list, obj, field):
        return any([type(obj) == type_ and field == field_ for type_, field_ in type_field_list])

    class FuckUEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj.__class__, DeclarativeMeta):
                fields = {}
                for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                    data = obj.__getattribute__(field)
                    if not in_list(blocklist, obj, field):
                        if jsonifiable(data) or in_list(allowlist, obj, field):
                            fields[field] = data
                        else:
                            fields[field] = None
                # a json-encodable dict
                return fields
            return json.JSONEncoder.default(self, obj)
    return FuckUEncoder

def fuckujson(obj):
    return json.dumps(
        obj,
        cls=nested_jsonifier([
            (server.data.test.Test, 'questions'),
            (server.data.question.Question, 'answers'),
            (server.data.people.People, 'exams'),
            (server.data.exam.Exam, 'answers'),
        ], [
            (server.data.people.People, 'password'),
            (server.data.people.People, 'set_password'),
            (server.data.people.People, 'get_password'),
        ]),
        check_circular=False
    )

class EasyAlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields
        return json.JSONEncoder.default(self, obj)


AlchemyEncoder = new_alchemy_encoder()


@app.route('/people', methods=['GET'])
def people_get():
    session = db_session.create_session()
    response_object = {'status': 'success'}
    response_object['people'] = session.query(People).all()
    # return jsonify(response_object)
    #return json.dumps(response_object, cls=new_alchemy_encoder(), check_circular=False)
    return fuckujson(response_object)


@app.route('/tests', methods=['GET'])
@jwt_required
def test_get():
    session = db_session.create_session()
    response_object = {'status': 'success'}
    response_object['tests'] = session.query(Test).all()
    #return json.dumps(response_object, cls=AlchemyEncoder, check_circular=False)
    return fuckujson(response_object)


@app.route('/tests/<id_test>', methods=['GET'])
def get_questions_test(id_test):
    session = db_session.create_session()
    response_object = {'status': 'success'}
    test = session.query(Test).filter(Test.id_test == id_test).first()
    response_object['questions'] = test.questions
    ids = [i.id_question for i in test.questions]
    response_object['another_questions'] = session.query(Question).filter(Question.id_question.notin_(ids)).all()
    return json.dumps(response_object, cls=AlchemyEncoder, check_circular=False)


@app.route('/questions', methods=['GET'])
def question_get():
    session = db_session.create_session()
    response_object = {'status': 'success'}
    response_object['questions'] = session.query(Question).all()
    return json.dumps(response_object, cls=AlchemyEncoder, check_circular=False)


@app.route('/answers/<id_question>', methods=['GET'])
def answer_get(id_question):
    session = db_session.create_session()
    response_object = {'status': 'success'}
    response_object['answer'] = session.query(Answer).filter(Answer.id_question == id_question).all()
    ret = json.dumps(response_object, cls=EasyAlchemyEncoder)
    return ret


@app.route('/exams', methods=['GET'])
@jwt_required
def exam_get():
    session = db_session.create_session()
    response_object = {'status': 'success'}
    response_object['exam'] = session.query(Exam).all()
    #return json.dumps(response_object, cls=AlchemyEncoder, check_circular=False)
    return fuckujson(response_object)

@app.route('/registration', methods=('POST',))
def register():
    session = db_session.create_session()
    response_object = {'status': 'success'}
    post_data = request.get_json()
    people = session.query(People).filter(People.username == post_data.get('username')).first()
    if not people:
        people = People(
            name=post_data['name'],
            group=post_data['group'],
            username=post_data['username']
        )
        people.set_password(post_data['password'])
        session.add(people)
        session.commit()
        response_object['message'] = 'Registration complete'
    else:
        response_object['message'] = 'Such username already exist. Try another one'
        response_object['status'] = False
    return jsonify(response_object)


@app.route('/login', methods=['GET', 'POST'])
def login():
    session = db_session.create_session()
    response_object = {'status': 'success'}
    post_data = request.get_json()
    user = session.query(People).filter(People.username == post_data['username']).first()
    if user and user.check_password(post_data['password']):
        response_object['message'] = 'Login successfully'
        access_token = create_access_token(identity=user.username)
        response_object['token'] = access_token
    else:
        response_object['message'] = 'Incorrect username/password'
        response_object['status'] = False
    return jsonify(response_object)


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


@app.route('/tests', methods=['POST'])
def test_post():
    session = db_session.create_session()
    post_data = request.get_json()
    response_object = {'status': 'success'}
    tests = session.query(Test).filter(post_data.get('id_test') == Test.id_test).all()
    if not tests:
        test = Test(
            max_mark=post_data.get('max_mark'),
            duration=post_data.get('duration'),
            test_name=post_data.get('test_name')
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


@app.route('/answers/<id_question>', methods=['POST'])
def answer_post(id_question):
    session = db_session.create_session()
    post_data = request.get_json()
    response_object = {'status': 'success'}
    answers = session.query(Answer).filter(post_data.get('id_answer') == Answer.id_answer).all()
    if not answers:
        answer = Answer(
            mark=post_data.get('mark'),
            answer_text=post_data.get('answer_text'),
            id_question=id_question
        )

        session.add(answer)
        session.commit()
        response_object['message'] = 'New answer created successfully'
    else:
        response_object['message'] = 'Such answer already exist'
    return jsonify(response_object)


@app.route('/am_i_logged', methods=['GET'])
@jwt_required
def am_i_logged():
    session = db_session.create_session()
    id_people = get_jwt_identity()
    return json.dumps({'name': session.query(People).filter(People.username == get_jwt_identity()).first().name})



@app.route('/exams', methods=['POST'])
@jwt_required
def exam_post():
    session = db_session.create_session()
    post_data = request.get_json()
    response_object = {'status': 'success'}
    id_people = get_jwt_identity()
    id_people = session.query(People).filter(People.username == get_jwt_identity()).first().id_people
    answers = session.query(Answer).filter(Answer.id_answer.in_(post_data['answers'].keys())).all()
    mark = sum([answer.mark for answer in answers])
    id_test = session.query(Test).filter(Test.test_name == post_data['test_name']).first().id_test
    exam = Exam(
        mark=mark,
        date=func.now(),
        id_people=id_people,
        answers=answers,
        id_test=id_test
    )
    session.add(exam)
    session.commit()
    response_object['message'] = 'New exam created successfully'
    return json.dumps(response_object, cls=AlchemyEncoder)


@app.route('/findtest/<test_name>', methods=['GET'])
def get_test_by_name(test_name):
    session = db_session.create_session()
    response_object = {'status': 'success'}
    test = session.query(Test).filter(test_name == Test.test_name).first()
    if test:
        response_object['test'] = test
    else:
        response_object['message'] = "No such test"
    return fuckujson(response_object) #json.dumps(response_object, cls=AlchemyEncoder, check_circular=False)


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


@app.route('/tests/<id_test>', methods=['PUT'])
def test_update(id_test):
    session = db_session.create_session()
    response_object = {'status': 'success'}
    put_data = request.get_json()
    test = session.query(Test).filter(Test.id_test == id_test).first()
    if test:
        if put_data.get('max_mark'):
            session.query(Test).filter(Test.id_test == id_test).update({
                'max_mark': put_data.get('max_mark'),
                'duration': put_data.get('duration'),
                'test_name': put_data.get('test_name')
            })
        if put_data.get('questions'):
            for i in put_data['questions']:
                test.questions.append(session.query(Question).filter(Question.id_question == i['id_question']).first())

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
            'max_mark': put_data.get('max_mark')
        })
        if put_data.get('answers'):
            for i in put_data['answers']:
                question.answers.append(session.query(Answer).filter(Answer.id_answer == i['id_answer']).first())
        session.commit()
        response_object['message'] = 'Question successfully updated'
    return jsonify(response_object)


@app.route('/answers/<id_answer>', methods=['PUT'])
def answer_update(id_answer):
    session = db_session.create_session()
    response_object = {'status': 'success'}
    put_data = request.get_json()
    answer = session.query(Answer).filter(Answer.id_answer == id_answer).first()
    if answer:
        session.query(Answer).filter(Answer.id_answer == id_answer).update({
            'answer_text': put_data.get('answer_text'),
            'mark': put_data.get('mark'),
            'id_question': put_data.get('id_question')
        })
        session.commit()
        response_object['message'] = 'Answer successfully updated'
    return jsonify(response_object)


@app.route('/exams/<id_exam>', methods=['PUT'])
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


@app.route('/tests/<id_test>', methods=['DELETE'])
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


@app.route('/answers/<id_answer>', methods=['DELETE'])
def answer_delete(id_answer):
    session = db_session.create_session()
    response_object = {'status': 'success'}
    answer = session.query(Answer).filter(Answer.id_answer == id_answer).first()
    if answer:
        session.delete(answer)
        session.commit()
        response_object['message'] = 'User successfully deleted'
    return jsonify(response_object)


@app.route('/exams/<id_exam>', methods=['DELETE'])
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
