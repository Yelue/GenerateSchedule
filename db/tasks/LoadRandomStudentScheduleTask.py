import pandas as pd 


class LoadRandomStudentScheduleTask:
	def __init__(self, engine):
		self.engine = engine

	def load_students(self):
		return pd.read_sql('select * from verif_student', con=self.engine)