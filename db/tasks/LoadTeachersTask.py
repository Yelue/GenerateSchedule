import csv
import pandas as pd
from db.tasks.BasicTask import BasicTask


class LoadTeachersTask(BasicTask):
	def __init__(self, engine):
		self.engine = engine

	def file_name(self):
		return 'table_teacher.csv'

	def get_data(self):
		return pd.read_csv(self.full_path(), sep='$', names=['teacher_long_name',
															'teacher_short_name',
															'teacher_degree',
															'teacher_short_degree'])

	def load_to_db(self):
		src = self.get_data()
		
		src.iloc[:,:-1].to_sql('teacher', con=self.engine, if_exists='append', index=False)