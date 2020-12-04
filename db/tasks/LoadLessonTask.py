import csv
import pandas as pd
from db.tasks.BasicTask import BasicTask


class LoadLessonTask(BasicTask):
	def __init__(self, engine):
		self.engine = engine

	def file_name(self):
		return 'table_lesson.csv'

	def get_data(self):
		return pd.read_csv(self.full_path(), sep='$', names=['lesson_short_name','lesson_long_name','lesson_type'])

	def load_to_db(self):
		src = self.get_data()
		src.to_sql('lesson', con=self.engine, if_exists='append', index=False)