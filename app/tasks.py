from db.tasks import LoadDaysTask, LoadDepartmentTask, \
						LoadFacultyTask, LoadGroupsTask, \
						LoadLessonTask, LoadTeachersTask, \
						LoadPairsTask, LoadCardTask,\
						LoadEmailStudents, LoadEmailTeachers,\
						LoadRandomTeacherScheduleTask,\
						LoadRandomStudentScheduleTask
from db.orm.tables import *


def load_db(engine):
	# LoadDaysTask.LoadDaysTask(engine=engine).load_to_db()
	# LoadFacultyTask.LoadFacultyTask(engine=engine).load_to_db()
	# LoadDepartmentTask.LoadDepartmentTask(engine=engine).load_to_db()
	# LoadGroupsTask.LoadGroupsTask(engine=engine).load_to_db()
	# LoadLessonTask.LoadLessonTask(engine=engine).load_to_db()
	# LoadTeachersTask.LoadTeachersTask(engine=engine).load_to_db()
	# LoadPairsTask.LoadPairsTask(engine=engine).load_to_db()
	# LoadCardTask.LoadCardTask(engine=engine).load_to_db()
	# LoadEmailStudents.LoadEmailStudents(engine=engine).load_to_db()
	# LoadEmailTeachers.LoadEmailTeachers(engine=engine).load_to_db()
	pass

def prepare_random_schedule(self):
	#prepare for teacher
	print(LoadRandomTeacherScheduleTask.LoadRandomTeacherScheduleTask(engine=engine).load_teachers())
	#prepare for student
	print(LoadRandomStudentScheduleTask.LoadRandomStudentScheduleTask(engine=engine).load_students())
	