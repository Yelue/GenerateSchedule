import pandas as pd 
import numpy as np
import random
from db.orm.tables import *


class LoadRandomStudentScheduleTask:
	def __init__(self, db):
		self.db = db

	def load_students(self):
		return pd.read_sql('select * from verif_student', con=self.db.engine)

	def load_to_db(self):
		self.create_schedule().to_sql('student_wish_schedule', con=self.db.engine, if_exists='append', index=False)
		
	def create_schedule(self):
		df_students = self.load_students()
		groups_id = tuple(df_students.group_id.values)
		df_cards = pd.read_sql(f'select * from card where group_id in {groups_id}', con=self.db.engine)
		df_cards = self.multiply_amount_time(df_cards)
		df_cards = self.prepare_data_db(df_cards, groups_id, df_students)

		return df_cards
	
	def multiply_amount_time(self, df_cards):

		return df_cards.loc[df_cards.index.repeat(df_cards.amount_time)].reset_index(drop=True)

	def prepare_data_db(self, df_cards, groups_id, df_students):
		pair_days = pd.DataFrame([(i,j) for j in range(1,6)for i in range(1,13)], columns=['day','para'])
		
		for t in groups_id:
			mask = df_cards.group_id==t

			sample_day_pair = pair_days.sample(len(df_cards[mask]))
			df_cards.loc[mask,['days_id','pairs_id']] = [tuple(x) for x in sample_day_pair.to_numpy()]
			df_cards.loc[mask,['st_secret_key']] =  [df_students[df_students.group_id==t].st_secret_key for _ in range(len(df_cards[mask]))]
		
		df_cards.drop(columns=['group_id','teacher_id','lesson_id','amount_time'], inplace=True)
		
		return df_cards