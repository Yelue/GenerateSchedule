import csv
import pandas as pd
from db.tasks.BasicTask import BasicTask

class LoadDaysTask(BasicTask):
	def __init__(self, engine):
		self.engine = engine

	def file_name(self):
		return 'table_days.csv'

	def get_data(self):
		return pd.read_csv(self.full_path(), sep='$', names=['name_day'])

	def load_to_db(self):
		self.get_data().to_sql('study_days', con=self.engine, if_exists='append', index=False)