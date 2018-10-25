#encoding:utf8

from .model import User, Token
from flask import jsonify, request
from sqlalchemy import and_, or_
from datetime import datetime

import hashlib
import sys
sys.path.append('../../')
from db import DBsession

from .. import api


@api.route('/user/login/', methods=['POST'])
def login():
    if not request.json:
        return jsonify({
            'code': 400,
            'message': 'param error'
        })
    try:
        session = DBsession()
        query = session.query(User).filter(and_(User.name == request.json['name'], User.password == request.json['password']))
        if(query.count() == 0):
            session.close()
            return jsonify({
                'code': 401,
                'message': '用户名不存在或密码错误',
            })
        else:
            m5 = hashlib.md5()
            m5.update((request.json['password'] + datetime.now().strftime('%Y%m%d%H%M%S')).encode(encoding='utf-8'))
            user = query.first().info()
            tokenStr = m5.hexdigest()
            token = Token(
                token = tokenStr,
                user_id = user['id'],
                create_time = int(datetime.now().strftime('%Y%m%d%H%M%S'))
            )
            session.query(Token).filter(Token.user_id == user['id']).delete()
            session.add(token)
            session.commit()
            session.close()
            return jsonify({
                'code': 200,
                'message': 'succ',
                'token': tokenStr
            })
    except Exception as err:
        print(err)
        return jsonify({
            'code': 400,
            'message': 'inner error'
        })
    # except Exception as err:
    #         logging.exception('error')
    #         return 

@api.route('/user/logout/', methods=['POST'])
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

@api.route('/user/', methods=['GET'])
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
