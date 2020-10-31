import csv
import pandas as pd
from db.tasks.BasicTask import BasicTask


class LoadPairsTask(BasicTask):
	def __init__(self, engine):
		self.engine = engine

	def file_name(self):
		return 'table_pairs.csv'

	def get_data(self):
		return pd.read_csv(self.full_path(), sep='$', names=['start_time','end_time'])

	def load_to_db(self):
		src = self.get_data()
		src.to_sql('pairs', con=self.engine, if_exists='append', index=False)