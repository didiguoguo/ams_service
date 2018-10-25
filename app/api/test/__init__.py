# encoding: utf8

from .model import Test
from flask import jsonify, request
from sqlalchemy import and_, or_
import sys
sys.path.append('../../')
from db import DBsession

from .. import api



@api.route('/tests/', methods=['GET'])
def get_tests():
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
        query = session.query(Test).filter(Test.id > 0)
        if request.args:
            if request.args.get('name',default = '') != '':
                query = query.filter(Test.name.like('%{e}%'.format(e=request.args['name'])))
            if request.args.get('work_type',default = '') != '':
                query = query.filter(Test.work_type.like('%{e}%'.format(e=request.args['work_type'])))
            response['pagination']['total'] = query.count()
            if request.args.get('current_page',default='') != '' and int(request.args['current_page']) > 0 and request.args.get('page_size',default='') != '' and int(request.args['page_size']) > 0:
                current_page = int(request.args['current_page'])
                page_size = int(request.args['page_size'])
                query = query.order_by(Test.id.desc()).limit(page_size).offset((current_page-1)*page_size)
            else:
                query = query.order_by(Test.id.desc())
        else:
            response['pagination']['total'] = query.count()
            response['pagination']['page_size'] = query.count()
            query = query.order_by(Test.id.desc())
        for i in query.all():
            response['list'].append(i.info())
        session.close()
        return jsonify(response)
    except:
        logging.exception('error')
        return 


@api.route('/test/<int:id>', methods=['GET'])
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


@api.route('/add/test/', methods=['POST'])
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


@api.route('/modify/test/<int:id>', methods=['PATCH'])
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


@api.route('/delete/tests/', methods=['DELETE'])
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
