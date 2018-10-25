#encoding:utf8

from sqlalchemy import Column, String, Integer
import sys
sys.path.append('../../')
from db import Base


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
