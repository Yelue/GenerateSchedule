import csv
import pandas as pd
from db.tasks.BasicTask import BasicTask

class LoadFacultyTask(BasicTask):
	def __init__(self, engine):
		self.engine = engine

	def file_name(self):
		return 'table_faculty.csv'

	def get_data(self):
		return pd.read_csv(self.full_path(), sep='$', names=['faculty_short_name', 'faculty_long_name'])

	def load_to_db(self):
		self.get_data().to_sql('faculty', con=self.engine, if_exists='append', index=False)