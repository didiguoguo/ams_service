# encoding: utf-8
import sys
sys.path.append('../../')
from .model import Classes
from flask import jsonify, request, Flask
from db import DBsession

from .. import api

@api.route('/classes/', methods=['GET'])
def get_classes():
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
        query = session.query(Classes).filter(Classes.id > 0)
        if request.args:
            if request.args.get('class_name',default = '') != '':
                query = query.filter(Classes.class_name.like('%{e}%'.format(e=request.args['class_name'])))
            response['pagination']['total'] = query.count()
            if request.args.get('current_page',default='') != '' and int(request.args['current_page']) > 0 and request.args.get('page_size',default='') != '' and int(request.args['page_size']) > 0:
                current_page = int(request.args['current_page'])
                page_size = int(request.args['page_size'])
                query = query.order_by(Classes.id.desc()).limit(page_size).offset((current_page-1)*page_size)
            else:
                query = query.order_by(Classes.id.desc())
        else:
            response['pagination']['total'] = query.count()
            response['pagination']['page_size'] = query.count()
            query = query.order_by(Classes.id.desc())
        for i in query.all():
            response['list'].append(i.info())
        session.close()
        return jsonify(response)
    except:
        logging.exception('error')
        return 


@api.route('/class/<int:id>', methods=['GET'])
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


@api.route('/add/class/', methods=['POST'])
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


@api.route('/modify/class/<int:id>', methods=['PATCH'])
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


@api.route('/delete/classes/', methods=['DELETE'])
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
