import csv
import pandas as pd
from db.tasks.BasicTask import BasicTask


class LoadCardTask(BasicTask):
	def __init__(self, engine):
		self.engine = engine

	def file_name(self):
		return 'table_cards.csv'

	def get_data(self):
		return pd.read_csv(self.full_path(), sep='$', names=['group_name',
															'lesson_short_name', 
															'teacher_long_name', 
															'lesson_type', 
															'amount_time'])

	def load_to_db(self):
		src = self.get_data()
		#work with groups
		group = pd.read_sql('select group_name, group_id from groups', con=self.engine)
		src = pd.merge(src, group, 
						how='left', 
						left_on='group_name', 
						right_on='group_name').drop(['group_name'],axis=1)
		del group
		#work with lesson
		lesson = pd.read_sql('select lesson_short_name, lesson_type, lesson_id from lesson', con=self.engine)
		src = pd.merge(src, lesson, 
						how='left', 
						left_on=['lesson_short_name', 'lesson_type'], 
						right_on=['lesson_short_name', 'lesson_type']).drop(['lesson_short_name', 
																				'lesson_type'],axis=1)
		del lesson
		#work with teacher
		teacher = pd.read_sql('select  teacher_long_name, teacher_id from teacher', con=self.engine)
		src = pd.merge(src, teacher, 
						how='left', 
						left_on=['teacher_long_name'], 
						right_on=['teacher_long_name']).drop(['teacher_long_name'], axis=1)
		src['teacher_id'].fillna(teacher[teacher.teacher_long_name=='None'].teacher_id[0], inplace=True)
		src.to_sql('card', con=self.engine, if_exists='append', index=False)