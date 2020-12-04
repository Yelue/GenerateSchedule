import sqlalchemy
import numpy as np
import pandas as pd
import requests
import os

from alg.population import Population
from alg.student_wishes import SWishesConnector
from alg.teacher_wishes import TWishesConnector
from alg.collection_cards import CollectionCards
from alg.genetic_algorithm import GeneticAlgorithm

from db.tasks import LoadDaysTask, LoadDepartmentTask, \
						LoadFacultyTask, LoadGroupsTask, \
						LoadLessonTask, LoadTeachersTask, \
						LoadPairsTask, LoadCardTask,\
						LoadEmailStudents, LoadEmailTeachers,\
						LoadRandomTeacherScheduleTask,\
						LoadRandomStudentScheduleTask,\
						LoadFullInfo, LoadFullSearchInfo
from db.orm.tables import *
import csv


def send_messages(db):
	urls = create_urls(db)
	for url in list(urls.keys())[:1]:
    	requests.post(
        	os.environ.get('MAIL_URL'),
        	auth=("api", os.environ.get("MAIL_API")),
        	data={"from": os.environ.get("MAIL_FROM"),
        		"to": "test <testrozklad@gmail.com>",
				"subject": "Hello",
				"text": "Email to edit schedule:%s"%urls[url]})

def create_urls(db):

	st_verif_query = "select * from verif_student;"
	tchr_verif_query = "select * from verif_teacher;"

	st_verif_df = pd.read_sql(st_verif_query, con=db.engine)
	tchr_verif_df = pd.read_sql(tchr_verif_query, con=db.engine)

	st_link = 'https://generateschedule.herokuapp.com/scheduledesign/student/' + st_verif_df.st_secret_key
	tchr_link = 'https://generateschedule.herokuapp.com/scheduledesign/teacher/' + tchr_verif_df.tchr_secret_key

	verif_teacher_links = {x: y for x,y in zip(tchr_verif_df.tchr_email, tchr_link)}
	verif_students_links = {x: y for x,y in zip(st_verif_df.st_email, st_link)}

	return {**verif_students_links, **verif_teacher_links}

def load_db(engine):
	LoadDaysTask.LoadDaysTask(engine=engine).load_to_db()
	LoadFacultyTask.LoadFacultyTask(engine=engine).load_to_db()
	LoadDepartmentTask.LoadDepartmentTask(engine=engine).load_to_db()
	LoadGroupsTask.LoadGroupsTask(engine=engine).load_to_db()
	LoadLessonTask.LoadLessonTask(engine=engine).load_to_db()
	LoadTeachersTask.LoadTeachersTask(engine=engine).load_to_db()
	LoadPairsTask.LoadPairsTask(engine=engine).load_to_db()
	LoadCardTask.LoadCardTask(engine=engine).load_to_db()
	LoadEmailStudents.LoadEmailStudents(engine=engine).load_to_db()
	LoadEmailTeachers.LoadEmailTeachers(engine=engine).load_to_db()
	

def prepare_random_schedule(db):
	#prepare for teacher
	LoadRandomTeacherScheduleTask.LoadRandomTeacherScheduleTask(db).load_to_db()
	#prepare for student
	LoadRandomStudentScheduleTask.LoadRandomStudentScheduleTask(db).load_to_db()
	

def prepare_schedule_interface(db, user_status, user_key):
	return LoadFullInfo.LoadFullInfo(db=db, user_status=user_status, user_key=user_key).create_schedule()

def prepare_data_db(data, user_status, user_key):
	data_db = []
	if user_status=='student':
		table = 'student_wish_schedule'
		column_key = 'st_secret_key'
	else:
		table = 'teacher_wish_schedule'
		column_key = 'tchr_secret_key'

	for lesson in data:
		data_db.append({
						column_key: user_key,
						'st_schedule_id': int(lesson['les_id']),
						'days_id': lesson['week']*6+lesson['day']+1,
						'pairs_id': lesson['les_num']+1})
	return data_db

def load_schedule_db(data,
					db,
					user_status,
					user_key):

	if user_status=='student':
		table = Student_Wish_Schedule
		column_key = 'st_schedule_id'
	else:
		table = Student_Wish_Schedule
		column_key = 'tchr_schedule_id'
	data = prepare_data_db(data=data,user_status=user_status,user_key=user_key)
	print(data)
	# for d in data:
	# 	db.session.query(table).filter_by(**{column_key:d[column_key]}).update(d)

	# db.session.commit()

def search_schedule(db, search_query):
	student = find_in_student(db, search_query)
	teacher = find_in_teacher(db, search_query)

	if student:
		#format_data
		return 'stud', LoadFullSearchInfo.LoadFullSearchInfo(db, user_status='student', ids=student).create_schedule()
	elif teacher:
		#format_data
		return 'teach', LoadFullSearchInfo.LoadFullSearchInfo(db, user_status='teacher', ids=teacher).create_schedule()

	return False
	
def check_schedule(db, search_query):
	student = find_in_student(db, search_query)
	teacher = find_in_teacher(db, search_query)

	return student or teacher


def find_in_student(db, search_query):
	try:
		group_id = db.session.query(Groups).filter_by(group_name=search_query).first().group_id
	except:
		return False
	cards_id = db.session.query(Card.card_id).filter_by(group_id=group_id).all()

	return db.session.query(Class.class_id).filter(Class.card_id.in_(cards_id)).all()


def find_in_teacher(db, search_query):
	try:
		teacher_id = db.session.query(Teacher).filter_by(teacher_short_name=search_query).first().teacher_id
	except:
		return False
	cards_id = db.session.query(Card.card_id).filter_by(teacher_id=teacher_id).all()
	
	return db.session.query(Class.class_id).filter(Class.card_id.in_(cards_id)).all()


def genetic_algorithm(db):
	print('Start work of genetic_algorithm')
	FACULTY_ID = 2
	rooms = np.array(range(1, 30))

	clc = CollectionCards(FACULTY_ID, db.session)
	swc = SWishesConnector(FACULTY_ID, db.session)
	twc = TWishesConnector(FACULTY_ID, db.session)

	ppl = Population(rooms, 100, FACULTY_ID, db.session)
	ppl.create_chromosomes()

	ga = GeneticAlgorithm(ppl.chromosomes, clc, swc, twc)
	ga.fit(n_iter = 3)

	classesL = []
	TB_chromosome = ga.chromosomes[0][0]
	for lesson in TB_chromosome.lessons:
		for card in lesson.cards:

			room, wdc = TB_chromosome.get_wdcByLessonNum(lesson.unNum)
			days_id = (wdc[0] + 1) * wdc[1] + 1
			pairs_id = wdc[2] + 1

			#classesL.append(Class(card_id = int(card), days_id = int(days_id), pairs_id = int(pairs_id)))
			# print('Card_id: {}, days_id: {}, pairs_id: {}'.format(card, days_id, pairs_id))

	#db.session.add_all(classesL)
	#db.session.commit()
	print('genetic_algorithm done')

def find_all_teachers(db):
	return [dict((col, getattr(row, col)) for col in row.__table__.columns.keys()) for row in db.session.query(Teacher).all()]


