from db.tasks import LoadDaysTask, LoadDepartmentTask, \
						LoadFacultyTask, LoadGroupsTask, \
						LoadLessonTask, LoadTeachersTask, \
						LoadPairsTask, LoadCardTask,\
						LoadEmailStudents, LoadEmailTeachers,\
						LoadRandomTeacherScheduleTask,\
						LoadRandomStudentScheduleTask,\
						LoadFullInfo, LoadFullSearchInfo
from db.orm.tables import *


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

def prepare_schedule_interface(db, user_status='student', user_key='$5$rounds=535000$qa5KMY9rGglSTjUc$iSsGfCyu1aHuDsM/5FYQhn/zfM1JCjueJml2kAmF6E6'):
	return LoadFullInfo.LoadFullInfo(db=db, user_status=user_status, user_key=user_key).create_schedule()

def prepare_data_db(data,
					user_status='student',
					user_key='$5$rounds=535000$qa5KMY9rGglSTjUc$iSsGfCyu1aHuDsM/5FYQhn/zfM1JCjueJml2kAmF6E6'):
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
					user_status='student',
					user_key='$5$rounds=535000$qa5KMY9rGglSTjUc$iSsGfCyu1aHuDsM/5FYQhn/zfM1JCjueJml2kAmF6E6'):
	if user_status=='student':
		table = Student_Wish_Schedule
		column_key = 'st_schedule_id'
	else:
		table = Student_Wish_Schedule
		column_key = 'tchr_schedule_id'

	data = prepare_data_db(data=data,user_status=user_status,user_key=user_key)
	for d in data:
		db.session.query(table).filter_by(**{column_key:d[column_key]}).update(d)

	db.session.commit()

def search_schedule(db, search_query):
	student = find_in_student(db, search_query)
	teacher = find_in_teacher(db, search_query)

	if student:
		#format_data
		return 'stud', LoadFullSearchInfo.LoadFullSearchInfo(db, user_status='student', ids=student).create_schedule()
	elif teacher:
		#format_data
		return 'teach', LoadFullSearchInfo.LoadFullSearchInfo(db, user_status='teacher', ids=teacher).create_schedule()


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
	return db.session.query(Student_Wish_Schedule.st_schedule_id).filter(Student_Wish_Schedule.card_id.in_(cards_id)).all()

def find_in_teacher(db, search_query):
	try:
		teacher_id = db.session.query(Teacher).filter_by(teacher_short_name=search_query).first().teacher_id
	except:
		return False
	cards_id = db.session.query(Card.card_id).filter_by(teacher_id=teacher_id).all()
	return db.session.query(Teacher_Wish_Schedule.tchr_schedule_id).filter(Teacher_Wish_Schedule.card_id.in_(cards_id)).all()
