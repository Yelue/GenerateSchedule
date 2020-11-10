import csv
import pandas as pd
from db.tasks.BasicTask import BasicTask
from passlib.hash import sha256_crypt
from random import randint


class LoadEmailTeachers(BasicTask):
	def __init__(self, engine):
		self.engine = engine

	def file_name(self):
		return 'table_verif_teachers.csv'

	def get_data(self):
		return pd.read_csv(self.full_path(), sep='$', names=['teacher_long_name','tchr_email'])

	def load_to_db(self):
		src = self.get_data()
		teacher = pd.read_sql('select  teacher_long_name, teacher_id from teacher', con=self.engine)
		src = pd.merge(src, teacher, 
						how='left', 
						left_on=['teacher_long_name'], 
						right_on=['teacher_long_name']).drop(['teacher_long_name'], axis=1)
		src['teacher_id'].fillna(teacher[teacher.teacher_long_name=='None'].teacher_id[0], inplace=True)
		
		src['tchr_secret_key'] = src['teacher_id'].apply(lambda x: sha256_crypt.encrypt(str(randint(1,100))))
		
		src.to_sql('verif_teacher', con=self.engine, if_exists='append', index=False)