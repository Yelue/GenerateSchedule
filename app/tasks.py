from db.tasks import LoadDaysTask, LoadDepartmentTask, \
						LoadFacultyTask, LoadGroupsTask, \
						LoadLessonTask, LoadTeachersTask, \
						LoadPairsTask, LoadCardTask

from db.orm.tables import *


def load_db(engine):
	# LoadDaysTask.LoadDaysTask(engine=engine).load_to_db()
	# LoadFacultyTask.LoadFacultyTask(engine=engine).load_to_db()
	# LoadDepartmentTask.LoadDepartmentTask(engine=engine).load_to_db()
	# LoadGroupsTask.LoadGroupsTask(engine=engine).load_to_db()
	# LoadLessonTask.LoadLessonTask(engine=engine).load_to_db()
	# LoadTeachersTask.LoadTeachersTask(engine=engine).load_to_db()
	# LoadPairsTask.LoadPairsTask(engine=engine).load_to_db()
	LoadCardTask.LoadCardTask(engine=engine).load_to_db()