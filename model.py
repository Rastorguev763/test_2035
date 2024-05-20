# model.py

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean, Text, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserInfo(Base):
    __tablename__ = 'user_info'
    user_ID = Column(Integer, primary_key=True)
    LeaderID = Column(Integer, unique=True, nullable=True)
    UntiID = Column(Integer, unique=True, nullable=True)
    lastname = Column(String(200))
    firstname = Column(String(200))
    middlename = Column(String(200))
    gender = Column(String(10))
    birthday = Column(DateTime)
    phone_LID = Column(String(20))
    phone_SEC = Column(String(20))
    mail_LID = Column(String(200))
    mail_SEC = Column(String(200))
    city = Column(String(255))
    country = Column(String(255))
    region = Column(String(255))
    is_verified = Column(Boolean)
    is_deleted = Column(Boolean)
    ts = Column(DateTime)

    facts = relationship("Fact", back_populates="user", cascade="all, delete, delete-orphan")
    fact_creators = relationship("FactCreator", back_populates="user", cascade="all, delete, delete-orphan")

class Fact(Base):
    __tablename__ = 'fact'
    fact_ID = Column(Integer, primary_key=True)
    user_ID = Column(Integer, ForeignKey('user_info.user_ID', ondelete="CASCADE"))
    source_ID = Column(Integer, ForeignKey('source.source_ID', ondelete="CASCADE"))
    fact_external_ID = Column(String(255))
    dict_fact_type_ID = Column(Integer)
    fact_start_date = Column(DateTime)
    fact_end_date = Column(DateTime)
    fact_title = Column(String(255))
    fact_description = Column(Text)
    fact_add_info = Column(Text)
    fact_string = Column(String(255))
    fact_tag = Column(String(50))
    is_teambased = Column(Boolean)
    is_deleted = Column(Boolean)
    ts = Column(DateTime)

    user = relationship("UserInfo", back_populates="facts")
    source = relationship("Source", back_populates="facts")
    fact_details = relationship("FactDetail", back_populates="fact", cascade="all, delete, delete-orphan")
    fact_creators = relationship("FactCreator", back_populates="fact", cascade="all, delete, delete-orphan")

class Source(Base):
    __tablename__ = 'source'
    source_ID = Column(Integer, primary_key=True)
    source_external_ID = Column(String(255))
    source_title = Column(String(255))
    source_description = Column(Text)
    source_add_info = Column(Text)
    is_deleted = Column(Boolean)
    ts = Column(DateTime)

    facts = relationship("Fact", back_populates="source", cascade="all, delete, delete-orphan")

class FactCreator(Base):
    __tablename__ = 'fact_creator'
    fact_creator_ID = Column(Integer, primary_key=True)
    fact_ID = Column(Integer, ForeignKey('fact.fact_ID', ondelete="CASCADE"))
    user_ID = Column(Integer, ForeignKey('user_info.user_ID', ondelete="CASCADE"))
    creator_role = Column(String(50))
    creator_description = Column(Text)
    creator_add_info = Column(Text)
    is_deleted = Column(Boolean)
    ts = Column(DateTime)

    fact = relationship("Fact", back_populates="fact_creators")
    user = relationship("UserInfo", back_populates="fact_creators")

class FactDetail(Base):
    __tablename__ = 'fact_detail'
    fact_detail_ID = Column(Integer, primary_key=True)
    fact_ID = Column(Integer, ForeignKey('fact.fact_ID', ondelete="CASCADE"))
    dict_detail_type_ID = Column(Integer, ForeignKey('dict_detail_type.dict_detail_type_ID', ondelete="CASCADE"))
    dict_result_value_type_ID = Column(Integer, ForeignKey('dict_result_value_type.dict_result_value_type_ID', ondelete="SET NULL"), nullable=True)
    result_scale_info_ID = Column(Integer, nullable=True)
    key = Column(String(255))
    value = Column(Text)
    add_info = Column(Text)
    is_deleted = Column(Boolean)
    ts = Column(DateTime)

    fact = relationship("Fact", back_populates="fact_details")
    dict_detail_type = relationship("DictDetailType")
    dict_result_value_type = relationship("DictResultValueType", foreign_keys=[dict_result_value_type_ID])

class DictResultValueType(Base):
    __tablename__ = 'dict_result_value_type'
    dict_result_value_type_ID = Column(Integer, primary_key=True)
    parental_value_type_ID = Column(Integer, nullable=True)
    title = Column(String(255))
    description = Column(Text)
    format = Column(Enum('type1', 'type2', 'type3', name='result_value_format_enum'))
    add_info = Column(Text)
    ts = Column(DateTime)

class DictDetailType(Base):
    __tablename__ = 'dict_detail_type'
    dict_detail_type_ID = Column(Integer, primary_key=True)
    title = Column(String(255))
    description = Column(Text)
    add_info = Column(Text)
    ts = Column(DateTime)
