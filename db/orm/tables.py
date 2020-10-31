from sqlalchemy import Column, Integer, Float, String, ForeignKey, Boolean, Time
from sqlalchemy.ext.declarative import declarative_base
from db.orm.engine import  engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

class Faculty(Base):
	__tablename__ = 'faculty'
	faculty_id = Column(Integer, primary_key=True)
	faculty_short_name = Column(String(20), nullable=True)
	faculty_long_name = Column(String(100), nullable=True)

	depart_faculty_id = relationship('Department', back_populates='depar_faculty_id')

class Department(Base):
	__tablename__ = 'department'

	department_id = Column(Integer, primary_key=True)
	department_short_name = Column(String(20), nullable=True)
	department_long_name = Column(String(100), nullable=True)
	faculty_id = Column(Integer, ForeignKey('faculty.faculty_id'))

	depar_faculty_id = relationship('Faculty', back_populates='depart_faculty_id')
	depar_group_id = relationship('Groups', back_populates='group_depar_id')

class Groups(Base):
	__tablename__ = 'groups'

	group_id = Column(Integer, primary_key=True)
	group_name = Column(String(10), nullable=True)
	group_course = Column(Integer, nullable=True)
	department_id = Column(Integer, ForeignKey('department.department_id'))

	group_depar_id = relationship('Department', back_populates='depar_group_id')
	# group_card_id = relationship('Card', back_populates='card_group_id')

class Teacher(Base):
	__tablename__ = 'teacher'

	teacher_id = Column(Integer, primary_key=True)
	teacher_short_name = Column(String(100), nullable=True)
	teacher_long_name = Column(String(100), nullable=True)
	teacher_degree = Column(String(100), nullable=True)

	# teacher_card_id = relationship('Card', back_populates='card_teacher_id')

class Lesson(Base):
	__tablename__ = 'lesson'

	lesson_id = Column(Integer, primary_key=True)

	lesson_short_name = Column(String(100), nullable=True)
	lesson_long_name = Column(String(100), nullable=True)
	lesson_type = Column(String(30), nullable=True)

	# lesson_card_id = relationship('Card', back_populates='card_lesson_id')

class Room(Base):
	__tablename__ = 'room'

	room_id = Column(Integer, primary_key=True)
	room_number = Column(Integer, nullable=True)
	room_type = Column(String(100), nullable=True)

	# room_class_id = relationship('Class', back_populates='class_room_id')

class Study_Days(Base):
	__tablename__ = 'study_days'

	days_id = Column(Integer, primary_key=True)
	name_day = Column(String(100), nullable=True)

	# days_class_id = relationship('Class', back_populates='class_days_id')

class Pairs(Base):
	__tablename__ = 'pairs'

	pairs_id = Column(Integer, primary_key=True)
	start_time = Column(Time, nullable=False)
	end_time = Column(Time, nullable=False)

	# pairs_class_id = relationship('Class', back_populates='class_pairs_id')

# class Card(Base):
# 	__tablename__ = 'card'

# 	card_id = Column(Integer, primary_key=True)
# 	group_id = Column(Integer, ForeignKey('group.group_id'))
# 	teacher_id = Column(Integer, ForeignKey('teacher.teacher_id'))
# 	lesson_id = Column(Integer, ForeignKey('lesson.lesson_id'))
# 	amount_id = Column(Integer, nullable=True)

# 	card_group_id = relationship('Group', back_populates='group_card_id')
# 	card_teacher_id = relationship('Teacher', back_populates='teacher_card_id')
# 	card_lesson_id = relationship('Lesson', back_populates='lesson_card_id')

# 	card_class_id = relationship('Class', back_populates='class_card_id')

# class Class(Base):
# 	__tablename__ = 'class'

# 	class_id = Column(Integer, primary_key=True)
# 	card_id = Column(Integer, ForeignKey('card.card_id'))
# 	room_id = Column(Integer, ForeignKey('room.room_id'))
# 	days_id = Column(Integer, ForeignKey('study_days.days_id'))
# 	pairs_id = Column(Integer, ForeignKey('pairs.pairs_id'))

# 	class_pairs_id = relationship('Pairs', back_populates='pairs_class_id')
# 	class_days_id = relationship('Study_Days', back_populates='days_class_id')
# 	class_room_id = relationship('Room', back_populates='room_class_id')
# 	class_card_id = relationship('Card', back_populates='card_class_id')

Base.metadata.create_all(engine)