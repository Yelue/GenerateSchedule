import pandas as pd 


class LoadRandomTeacherScheduleTask:
	def __init__(self, engine):
		self.engine = engine

	def load_teachers(self):
		print('kuku')
		return pd.read_sql('select * from verif_teacher', con=self.engine)