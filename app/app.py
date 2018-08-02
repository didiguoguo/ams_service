from flask import Flask
from flask import request
from flask import jsonify
from flask import abort
from flask_cors import CORS
from sqlalchemy import and_, or_
from datetime import datetime
import logging
import hashlib
logging.basicConfig(level=logging.INFO)

from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer(), primary_key=True)
    name = Column(String(64))
    email = Column(String(64))
    password = Column(String(16))

    def info(self):
        return dict(id=self.id,
                    name=self.name,
                    email=self.email,
                    )


class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer(), primary_key=True, nullable=False)
    student_name = Column(String(64), nullable=False)
    gender = Column(Integer())
    id_card_num = Column(Integer(), nullable=False)
    phone_num = Column(Integer(), nullable=False)
    job_title = Column(String(64))
    enter_time = Column(Integer())
    class_id = Column(Integer())
    class_name = Column(String(64))
    theory_result = Column(Integer())
    practise_result = Column(Integer())

    def info(self):
        return dict(id=self.id,
                    student_name=self.student_name,
                    gender=self.gender,
                    id_card_num=self.id_card_num,
                    phone_num=self.phone_num,
                    job_title=self.job_title,
                    enter_time=self.enter_time,
                    class_id=self.class_id,
                    class_name=self.class_name,
                    theory_result=self.theory_result,
                    practise_result=self.practise_result
                    )


class Classes(Base):
    __tablename__ = 'class'
    id = Column(Integer(), primary_key=True, nullable=False)
    class_name = Column(String(64), nullable=False)
    begin_address = Column(String(128))
    begin_time = Column(Integer())
    end_time = Column(Integer())
    course_plan = Column(String(128))
    create_time = Column(Integer())

    def info(self):
        return dict(id=self.id,
                    class_name=self.class_name,
                    begin_address=self.begin_address,
                    begin_time=self.begin_time,
                    end_time=self.end_time,
                    create_time=self.create_time,
                    course_plan=self.course_plan,
                    )


class Test(Base):
    __tablename__ = 'test'
    id = Column(Integer(), primary_key=True, nullable=False)
    name = Column(String(64), nullable=False)
    type = Column(String(20))
    work_type = Column(String(20))
    target_name = Column(String(128))
    target_id = Column(Integer())
    start_time = Column(Integer())
    create_time = Column(Integer())
    end_time = Column(Integer())
    duration = Column(Integer())
    times = Column(Integer())
    status = Column(String(10))

    def info(self):
        return dict(id=self.id,
                    name=self.name,
                    type=self.type,
                    work_type=self.work_type,
                    target_name=self.target_name,
                    target_id=self.target_id,
                    start_time=self.start_time,
                    end_time=self.end_time,
                    create_time=self.create_time,
                    duration=self.duration,
                    times=self.times,
                    status=self.status
                    )


class Token(Base):
    __tablename__ = 'token'
    user_id = Column(Integer(), primary_key=True, nullable=False)
    token = Column(String(64), nullable=False)
    create_time = Column(Integer())

    def info(self):
        return dict(user_id=self.user_id,
                    token=self.token,
                    create_time=self.create_time,
                    )

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/students/', methods=['GET'])
def get_students():
    if not request.headers.get('token',None):
        return jsonify({
            'code': 401,
            'message': '用户没有权限（令牌、用户名、密码错误）。'
        })
    current_page = 1
    page_size = 10
    total = 0
    try:
        response = {
            'list': [],
            'code': 200,
            'message': 'succ',
            'pagination': {
                'current_page': current_page,
                'page_size': page_size,
                'total': total,
            }
        }
        session = DBsession()
        query = session.query(Student).filter(Student.id > 0)
        result = None
        if request.args:
            if request.args.get('student_name',default = '') != '':
                query = query.filter(or_(
                    Student.student_name.like('%{e}%'.format(e=request.args['student_name'])),
                    Student.id_card_num.like('%{e}%'.format(e=request.args['student_name'])),
                    ))
            if request.args.get('id_card_num',default = '') != '':
                query = query.filter(Student.id_card_num == request.args['id_card_num'])
            if request.args.get('class_id',default = '') != '':
                query = query.filter(Student.class_id == request.args['class_id'])
            response['pagination']['total'] = query.count()
            if request.args.get('current_page',default='') != '' and int(request.args['current_page']) > 0 and request.args.get('page_size',default='') != '' and int(request.args['page_size']) > 0:
                current_page = int(request.args['current_page'])
                page_size = int(request.args['page_size'])
                result = query.order_by(Student.id.desc()).limit(page_size).offset((current_page-1)*page_size).all()
        else:
            response['pagination']['total'] = query.count()
            response['pagination']['page_size'] = query.count()
            result = query.order_by(Student.id.desc()).all()
        for i in result:
            response['list'].append(i.info())
        session.close()
        return jsonify(response)
    except Exception as err:
        logging.exception('error')
        return 


@app.route('/student/<int:id>', methods=['GET'])
def get_student_by_id(id):
    if not request.headers.get('token',None):
        return jsonify({
            'code': 401,
            'message': '用户没有权限（令牌、用户名、密码错误）。'
        })
    try:
        response = {
            'data': {},
            'code': 200,
            'message': 'succ',
        }
        session = DBsession()
        response['data'] = session.query(
            Student).filter_by(id=id).first().info()
        session.close()
        return jsonify(response)
    except:
        return


@app.route('/add/student/', methods=['POST'])
def add_student():
    if not request.headers.get('token',None):
        return jsonify({
            'code': 401,
            'message': '用户没有权限（令牌、用户名、密码错误）。'
        })
    if not request.json:
        return jsonify({
            'code': 400,
            'message': 'param error'
        })
    try:
        student = Student(
            student_name=request.json['student_name'],
            gender=request.json['gender'],
            phone_num=request.json['phone_num'],
            id_card_num=request.json['id_card_num'],
            job_title=request.json['job_title'],
            enter_time=datetime.now().strftime('%Y%m%d%H%M%S')
        )
        session = DBsession()
        session.add(student)
        session.commit()
        session.close()
        return jsonify({
            'code': 200,
            'message': 'succ',
        })
    except:
        return jsonify({
            'code': 400,
            'message': 'param error'
        })


@app.route('/modify/student/<int:id>', methods=['PATCH'])
def modify_student(id):
    if not request.headers.get('token',None):
        return jsonify({
            'code': 401,
            'message': '用户没有权限（令牌、用户名、密码错误）。'
        })
    if not request.json or not id:
        return jsonify({
            'code': 400,
            'message': 'param error'
        })
    try:
        session = DBsession()
        for k, v in request.json.items():
            if k and v:
                session.query(Student).filter(Student.id == id).update({k: v})
        session.commit()
        session.close()
        return jsonify({
            'code': 200,
            'message': 'succ',
        })
    except:
        return jsonify({
            'code': 400,
            'message': 'inner error'
        })


@app.route('/delete/students/', methods=['DELETE'])
def delete_students():
    if not request.headers.get('token',None):
        return jsonify({
            'code': 401,
            'message': '用户没有权限（令牌、用户名、密码错误）。'
        })
    if not request.json:
        return jsonify({
            'code': 400,
            'message': 'param error'
        })
    try:
        session = DBsession()
        session.query(Student).filter(Student.id.in_(
            request.json['ids'])).delete(synchronize_session=False)
        session.commit()
        session.close()
        return jsonify({
            'code': 200,
            'message': 'succ',
        })
    except:
        return jsonify({
            'code': 404,
            'message': 'Not Found'
        })


@app.route('/classes/', methods=['GET'])
def get_classes():
    if not request.headers.get('token',None):
        return jsonify({
            'code': 401,
            'message': '用户没有权限（令牌、用户名、密码错误）。'
        })
    current_page = 1
    page_size = 10
    total = 0
    result = None
    try:
        response = {
            'list': [],
            'code': 200,
            'message': 'succ',
            'pagination': {
                'current_page': current_page,
                'page_size': page_size,
                'total': total,
            }
        }
        session = DBsession()
        query = session.query(Classes).filter(Classes.id > 0)
        if request.args:
            if request.args.get('class_name',default = '') != '':
                query = query.filter(Classes.class_name.like('%{e}%'.format(e=request.args['class_name'])))
            response['pagination']['total'] = query.count()
            if request.args.get('current_page',default='') != '' and int(request.args['current_page']) > 0 and request.args.get('page_size',default='') != '' and int(request.args['page_size']) > 0:
                current_page = int(request.args['current_page'])
                page_size = int(request.args['page_size'])
                result = query.order_by(Classes.id.desc()).limit(page_size).offset((current_page-1)*page_size).all()
        else:
            response['pagination']['total'] = query.count()
            response['pagination']['page_size'] = query.count()
            result = query.order_by(Classes.id.desc()).all()
        for i in result:
            response['list'].append(i.info())
        session.close()
        return jsonify(response)
    except:
        logging.exception('error')
        return 


@app.route('/class/<int:id>', methods=['GET'])
def get_class_by_id(id):
    if not request.headers.get('token',None):
        return jsonify({
            'code': 401,
            'message': '用户没有权限（令牌、用户名、密码错误）。'
        })
    try:
        response = {
            'data': {},
            'code': 200,
            'message': 'succ',
        }
        session = DBsession()
        response['data'] = session.query(
            Classes).filter_by(id=id).first().info()
        session.close()
        return jsonify(response)
    except:
        return


@app.route('/add/class/', methods=['POST'])
def add_class():
    if not request.headers.get('token',None):
        return jsonify({
            'code': 401,
            'message': '用户没有权限（令牌、用户名、密码错误）。'
        })
    if not request.json:
        return jsonify({
            'code': 400,
            'message': 'param error'
        })
    try:
        cla = Classes(
            class_name=request.json['class_name'],
            begin_time=int(request.json['begin_time']),
            end_time=int(request.json['end_time']),
            begin_address=request.json['begin_address'],
            course_plan=request.json['course_plan'],
            create_time=int(datetime.now().strftime('%Y%m%d%H%M%S'))
        )
        session = DBsession()
        session.add(cla)
        session.commit()
        session.close()
        return jsonify({
            'code': 200,
            'message': 'succ',
        })
    except:
        return jsonify({
            'code': 400,
            'message': 'server error'
        })


@app.route('/modify/class/<int:id>', methods=['PATCH'])
def modify_class(id):
    if not request.headers.get('token',None):
        return jsonify({
            'code': 401,
            'message': '用户没有权限（令牌、用户名、密码错误）。'
        })
    if not request.json or not id:
        return jsonify({
            'code': 400,
            'message': 'param error'
        })
    try:
        session = DBsession()
        for k, v in request.json.items():
            if k and v:
                session.query(Classes).filter(Classes.id == id).update({k: v})
        session.commit()
        session.close()
        return jsonify({
            'code': 200,
            'message': 'succ',
        })
    except:
        return jsonify({
            'code': 400,
            'message': 'inner error'
        })


@app.route('/delete/classes/', methods=['DELETE'])
def delete_classes():
    if not request.headers.get('token',None):
        return jsonify({
            'code': 401,
            'message': '用户没有权限（令牌、用户名、密码错误）。'
        })
    if not request.json:
        return jsonify({
            'code': 400,
            'message': 'param error'
        })
    try:
        session = DBsession()
        session.query(Classes).filter(Classes.id.in_(
            request.json['ids'])).delete(synchronize_session=False)
        session.commit()
        session.close()
        return jsonify({
            'code': 200,
            'message': 'succ',
        })
    except:
        return jsonify({
            'code': 404,
            'message': 'Not Found'
        })




@app.route('/tests/', methods=['GET'])
def get_tests():
    if not request.headers.get('token',None):
        return jsonify({
            'code': 401,
            'message': '用户没有权限（令牌、用户名、密码错误）。'
        })
    current_page = 1
    page_size = 10
    total = 0
    result = None
    try:
        response = {
            'list': [],
            'code': 200,
            'message': 'succ',
            'pagination': {
                'current_page': current_page,
                'page_size': page_size,
                'total': total,
            }
        }
        session = DBsession()
        query = session.query(Test).filter(Test.id > 0)
        if request.args:
            if request.args.get('name',default = '') != '':
                query = query.filter(Test.name.like('%{e}%'.format(e=request.args['name'])))
            response['pagination']['total'] = query.count()
            if request.args.get('current_page',default='') != '' and int(request.args['current_page']) > 0 and request.args.get('page_size',default='') != '' and int(request.args['page_size']) > 0:
                current_page = int(request.args['current_page'])
                page_size = int(request.args['page_size'])
                result = query.order_by(Test.id.desc()).limit(page_size).offset((current_page-1)*page_size).all()
        else:
            response['pagination']['total'] = query.count()
            response['pagination']['page_size'] = query.count()
            result = query.order_by(Test.id.desc()).all()
        for i in result:
            response['list'].append(i.info())
        session.close()
        return jsonify(response)
    except:
        logging.exception('error')
        return 


@app.route('/test/<int:id>', methods=['GET'])
def get_by_id(id):
    if not request.headers.get('token',None):
        return jsonify({
            'code': 401,
            'message': '用户没有权限（令牌、用户名、密码错误）。'
        })
    try:
        response = {
            'data': {},
            'code': 200,
            'message': 'succ',
        }
        session = DBsession()
        response['data'] = session.query(
            Test).filter_by(id=id).first().info()
        session.close()
        return jsonify(response)
    except:
        return


@app.route('/add/test/', methods=['POST'])
def add_test():
    if not request.headers.get('token',None):
        return jsonify({
            'code': 401,
            'message': '用户没有权限（令牌、用户名、密码错误）。'
        })
    if not request.json:
        return jsonify({
            'code': 400,
            'message': 'param error'
        })
    try:
        test = Test(
            name = request.json['name'],
            type = request.json['type'],
            target_id = request.json['target_id'],
            duration = int(request.json['duration']),
            times = int(request.json['times']),
            work_type = request.json['work_type'],
            start_time = int(request.json['cycle'][0]),
            end_time = int(request.json['cycle'][1]),
            create_time = int(datetime.now().strftime('%Y%m%d%H%M%S'))
        )
        session = DBsession()
        session.add(test)
        session.commit()
        session.close()
        return jsonify({
            'code': 200,
            'message': 'succ',
        })
    except:
        return jsonify({
            'code': 400,
            'message': 'server error'
        })


@app.route('/modify/test/<int:id>', methods=['PATCH'])
def modify_test(id):
    if not request.headers.get('token',None):
        return jsonify({
            'code': 401,
            'message': '用户没有权限（令牌、用户名、密码错误）。'
        })
    if not request.json or not id:
        return jsonify({
            'code': 400,
            'message': 'param error'
        })
    try:
        session = DBsession()
        for k, v in request.json.items():
            if k and v:
                session.query(Test).filter(Test.id == id).update({k: v})
        session.commit()
        session.close()
        return jsonify({
            'code': 200,
            'message': 'succ',
        })
    except:
        return jsonify({
            'code': 400,
            'message': 'inner error'
        })


@app.route('/delete/tests/', methods=['DELETE'])
def delete_tests():
    if not request.headers.get('token',None):
        return jsonify({
            'code': 401,
            'message': '用户没有权限（令牌、用户名、密码错误）。'
        })
    if not request.json:
        return jsonify({
            'code': 400,
            'message': 'param error'
        })
    try:
        session = DBsession()
        session.query(Test).filter(Test.id.in_(
            request.json['ids'])).delete(synchronize_session=False)
        session.commit()
        session.close()
        return jsonify({
            'code': 200,
            'message': 'succ',
        })
    except:
        return jsonify({
            'code': 404,
            'message': 'Not Found'
        })

@app.route('/user/login/', methods=['POST'])
def login():
    if not request.json:
        return jsonify({
            'code': 400,
            'message': 'param error'
        })
    try:
        session = DBsession()
        query = session.query(Test).filter(and_(User.name == request.json['name'], User.password == request.json['password']))
        if(query.count() == 0):
            session.close()
            return jsonify({
                'code': 401,
                'message': '用户名不存在或密码错误',
            })
        else:
            m5 = hashlib.md5()
            m5.update(request.json['password'].encode(encoding='utf-8'))
            user = query.first().info()
            tokenStr = m5.hexdigest()
            token = Token(
                token = tokenStr,
                user_id = user['id'],
                create_time = int(datetime.now().strftime('%Y%m%d%H%M%S'))
            )
            session.query(Token).filter(Token.user_id == token.user_id).delete()
            session.add(token)
            session.commit()
            session.close()
            return jsonify({
                'code': 200,
                'message': 'succ',
                'token': tokenStr
            })
    except:
        return jsonify({
            'code': 400,
            'message': 'inner error'
        })
    # except Exception as err:
    #         logging.exception('error')
    #         return 

@app.route('/user/logout/', methods=['POST'])
def logout():
    if not request.headers.get('token', None):
        return jsonify({
            'code': 401,
            'message': '用户没有权限（令牌、用户名、密码错误）。'
        })
    try:
        session = DBsession()
        session.query(Token).filter(Token.token == request.headers.get('token', None)).delete()
        session.commit()
        session.close()
        return jsonify({
            'code': 200,
            'message': 'succ'
        })
    except:
        return jsonify({
            'code': 400,
            'message': 'inner error'
        })

@app.route('/user/', methods=['GET'])
def get_user():
    token = request.headers.get('token', None)
    if not token:
        return jsonify({
            'code': 401,
            'message': '用户没有权限（令牌、用户名、密码错误）。'
        })
    else: 
        try:
            response = {
                'data': {},
                'code': 200,
                'message': 'succ',
            }
            session = DBsession()
            token_data = session.query(Token).filter(Token.token == token).first()
            if not token_data:
                return jsonify({
                    'code': 401,
                    'message': '用户没有权限（令牌、用户名、密码错误）。'
                })
            response['data'] = session.query(User).filter(User.id == token_data.user_id).first().info()
            session.close()
            return jsonify(response)
        except Exception as err:
            logging.exception('error')
            return 


if __name__ == '__main__':
    engine = create_engine(
        'mysql+mysqlconnector://root:password@localhost:3306/ams')
    DBsession = sessionmaker(bind=engine)
    app.run(host="192.168.1.14", port=5000, debug=True)
