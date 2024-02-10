from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

# Определение моделей данных для предметов, преподавателей, кабинетов и расписания с использованием SQLAlchemy.

# Базовый класс для всех моделей.
Base = declarative_base()

engine = create_engine('sqlite:///school_schedule.db')
Session = sessionmaker(bind=engine)

# Модель предмета с полями для названия.
class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    schedules = relationship('Schedule', back_populates='subject')

# Модель препода с полями для имени.
class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    schedules = relationship('Schedule', back_populates='teacher')

# Модель кабинета с полями для номера и вместимости.
class Classroom(Base):
    __tablename__ = 'classrooms'
    id = Column(Integer, primary_key=True)
    number = Column(Integer, unique=True, nullable=False)
    capacity = Column(Integer, nullable=False)
    schedules = relationship('Schedule', back_populates='classroom')

# Модель расписания, связывающая предметы, преподавателей и кабинеты.
class Schedule(Base):
    __tablename__ = 'schedules'
    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=False)
    classroom_id = Column(Integer, ForeignKey('classrooms.id'), nullable=False)
    hidden = Column(Boolean, default=False) 
    subject = relationship('Subject', back_populates='schedules')
    teacher = relationship('Teacher', back_populates='schedules')
    classroom = relationship('Classroom', back_populates='schedules')


Base.metadata.create_all(engine)
