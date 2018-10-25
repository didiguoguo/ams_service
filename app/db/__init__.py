from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = create_engine(
    'mysql+mysqldb://root:password@10.10.28.14:3306/ams?charset=utf8'
)
DBsession = sessionmaker(bind=engine)
