import csv
import pandas as pd
from db.tasks.BasicTask import BasicTask
from passlib.hash import sha256_crypt
from random import randint


class LoadEmailStudents(BasicTask):
	def __init__(self, engine):
		self.engine = engine

	def file_name(self):
		return 'table_verif_students.csv'

	def get_data(self):
		return pd.read_csv(self.full_path(), sep='$', names=['group_name','st_email'])

	def load_to_db(self):
		src = self.get_data()
		group = pd.read_sql('select group_name, group_id from groups', con=self.engine)
		src = pd.merge(src, group, 
						how='left', 
						left_on='group_name', 
						right_on='group_name').drop(['group_name'],axis=1)
		src['st_secret_key'] = src['group_id'].apply(lambda x: sha256_crypt.encrypt(str(randint(1,100))))
		
		src.to_sql('verif_student', con=self.engine, if_exists='append', index=False)