import csv
import pandas as pd
from db.tasks.BasicTask import BasicTask


class LoadDepartmentTask(BasicTask):
	def __init__(self, engine):
		self.engine = engine

	def file_name(self):
		return 'table_depart.csv'

	def get_data(self):
		return pd.read_csv(self.full_path(), sep='$', names=['department_short_name','department_long_name','faculty'])

	def load_to_db(self):
		src = self.get_data()
		exi = pd.read_sql('select * from faculty', con=self.engine).loc[:,['faculty_short_name','faculty_id']]
		src = pd.merge(src, exi, 
						how='left', 
						left_on='faculty', 
						right_on='faculty_short_name').drop(['faculty_short_name','faculty'],
						axis=1)
		
		src.to_sql('department', con=self.engine, if_exists='append', index=False)