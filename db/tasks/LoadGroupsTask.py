import csv
import pandas as pd
from db.tasks.BasicTask import BasicTask


class LoadGroupsTask(BasicTask):
	def __init__(self, engine):
		self.engine = engine

	def file_name(self):
		return 'table_groups.csv'

	def get_data(self):
		return pd.read_csv(self.full_path(), sep='$', names=['group_name','group_course','department'])

	def load_to_db(self):
		src = self.get_data()
		exi = pd.read_sql('select department_short_name,department_id from department', con=self.engine)
		src = pd.merge(src, exi, 
						how='left', 
						left_on='department', 
						right_on='department_short_name').drop(['department_short_name','department'],
						axis=1)
		
		src.to_sql('groups', con=self.engine, if_exists='append', index=False)