from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

# Создаем базовый класс для моделей, используя декларативный стиль SQLAlchemy.
Base = declarative_base()

# Настраиваем подключение к базе данных SQLite. Путь к файлу DB указан относительно скрипта.
engine = create_engine('sqlite:///school_schedule.db')

# Создаем фабрику сессий, привязанную к нашему движку базы данных.
Session = sessionmaker(bind=engine)

# Определение модели Subject для представления предметов в базе данных.
class Subject(Base):
    __tablename__ = 'subjects'  # Название таблицы в базе данных.
    id = Column(Integer, primary_key=True)  # Уникальный идентификатор предмета.
    name = Column(String, unique=True, nullable=False)  # Название предмета. Должно быть уникальным.
    schedules = relationship('Schedule', back_populates='subject')  # Связь с расписанием.

# Определение модели Teacher для представления преподавателей.
class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)  # Уникальный идентификатор преподавателя.
    name = Column(String, nullable=False)  # Имя преподавателя.
    schedules = relationship('Schedule', back_populates='teacher')  # Связь с расписанием.

# Определение модели Classroom для представления кабинетов.
class Classroom(Base):
    __tablename__ = 'classrooms'
    id = Column(Integer, primary_key=True)  # Уникальный идентификатор кабинета.
    number = Column(Integer, unique=True, nullable=False)  # Номер кабинета. Должен быть уникальным.
    capacity = Column(Integer, nullable=False)  # Вместимость кабинета.
    schedules = relationship('Schedule', back_populates='classroom')  # Связь с расписанием.

# Определение модели Schedule для представления расписания.
class Schedule(Base):
    __tablename__ = 'schedules'
    id = Column(Integer, primary_key=True)  # Уникальный идентификатор записи расписания.
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)  # Внешний ключ к предмету.
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=False)  # Внешний ключ к преподавателю.
    classroom_id = Column(Integer, ForeignKey('classrooms.id'), nullable=False)  # Внешний ключ к кабинету.
    hidden = Column(Boolean, default=False)  # Флаг, указывающий, скрыта ли запись расписания.
    date = Column(Date, nullable=False)  # Дата проведения урока.
    # Обратные связи для навигации по модели.
    subject = relationship("Subject", back_populates="schedules")
    teacher = relationship("Teacher", back_populates="schedules")
    classroom = relationship("Classroom", back_populates="schedules")

# Создаем все таблицы в базе данных, основываясь на определениях моделей.
Base.metadata.create_all(engine)
