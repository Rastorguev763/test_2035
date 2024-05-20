# main.py

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from model import (
    UserInfo,
    Fact,
    Source,
    FactCreator,
    FactDetail,
    DictResultValueType,
    DictDetailType,
    Base,
    )

# Создание сессии и базы данных
engine = create_engine('sqlite:///example.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()