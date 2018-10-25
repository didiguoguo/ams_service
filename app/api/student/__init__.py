# encoding: utf8

from datetime import datetime
from .model import Student
from flask import jsonify, request
from sqlalchemy import and_, or_

import sys
sys.path.append('../../')
from db import DBsession

from .. import api

@api.route('/students/', methods=['GET'])
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
                query = query.order_by(Student.id.desc()).limit(page_size).offset((current_page-1)*page_size)
            else:
                query = query.order_by(Student.id.desc())
        else:
            response['pagination']['total'] = query.count()
            response['pagination']['page_size'] = query.count()
            query = query.order_by(Student.id.desc())
        for i in query.all():
            print i.info()
            response['list'].append(i.info())
        session.close()
        return jsonify(response)
    except Exception as err:
        logging.exception('error')
        return 


@api.route('/student/<int:id>', methods=['GET'])
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


@api.route('/add/student/', methods=['POST'])
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
    except Exception as err:
	print(err)
        return jsonify({
            'code': 400,
            'message': 'param error'
        })


@api.route('/modify/student/<int:id>', methods=['PATCH'])
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


@api.route('/delete/students/', methods=['DELETE'])
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



