from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from models import Base, Subject, Teacher, Classroom, Schedule

# Настройка подключения к базе данных SQLite.
engine = create_engine('sqlite:///school_schedule.db')
Session = sessionmaker(bind=engine)

# Функция инициализации базы данных. Создает таблицы и заполняет начальными данными.
def init_db():
    # Проверка существующих записей и добавление новых при необходимости.
    session = Session()
    existing_numbers = [c[0] for c in session.query(Classroom.number).all()]

    classrooms = [
        Classroom(number=101, capacity=30),
        Classroom(number=102, capacity=20),
        Classroom(number=103, capacity=25),
    ]

    for classroom in classrooms:
        if classroom.number not in existing_numbers:
            session.add(classroom)

    try:
        session.commit()
    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")
        session.rollback()
    finally:
        session.close()


# Функция добавления урока в расписание.
def add_schedule_entry(subject_name, teacher_names, classroom_number):
     # Добавление урока с проверкой на существование всех связанных сущностей.
    session = Session()
    subject = session.query(Subject).filter_by(name=subject_name).first()
    if not subject:
        subject = Subject(name=subject_name)
        session.add(subject)
        session.commit()

    classroom = session.query(Classroom).filter_by(number=classroom_number).first()
    if not classroom:
        print(f"Кабинет {classroom_number} не найден.")
        return

    teachers = []
    for name in teacher_names.split(', '):
        teacher = session.query(Teacher).filter_by(name=name).first()
        if not teacher:
            teacher = Teacher(name=name)
            session.add(teacher)
            session.commit()
        teachers.append(teacher)

    for teacher in teachers:
        new_schedule = Schedule(subject_id=subject.id, teacher_id=teacher.id, classroom_id=classroom.id)
        session.add(new_schedule)
    
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Ошибка при добавлении урока: {e}")
    finally:
        session.close()

# Функция получения актуального расписания на сегодня.
def get_today_schedule():
    # Возврат списка уроков, исключая скрытые.
    session = Session()
    schedules = session.query(Schedule).join(Subject).join(Teacher).join(Classroom).filter(Schedule.hidden == False).order_by(Schedule.id).all()
    schedule_list = []
    for index, schedule in enumerate(schedules, start=1):
        schedule_info = (f"Урок {index}: Предмет: {schedule.subject.name}, "
                         f"Преподаватель: {schedule.teacher.name}, "
                         f"Кабинет: {schedule.classroom.number}")
        schedule_list.append(schedule_info)
    session.close()
    return schedule_list

# Функция скрытия урока из расписания.
def hide_schedule(lesson_number):
    # Скрытие урока по его порядковому номеру в списке активных уроков.
    session = Session()
    visible_schedules = session.query(Schedule).filter_by(hidden=False).order_by(Schedule.id).all()

    if lesson_number > len(visible_schedules) or lesson_number < 1:
        return "Неверный номер урока."

    schedule_to_hide = visible_schedules[lesson_number - 1] 
    schedule_to_hide.hidden = True
    
    try:
        session.commit()
        return "Урок успешно скрыт из расписания."
    except Exception as e:
        session.rollback()
        return f"Ошибка при скрытии урока: {e}"
    finally:
        session.close()

