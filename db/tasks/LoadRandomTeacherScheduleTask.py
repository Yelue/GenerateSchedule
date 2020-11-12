import pandas as pd 
import numpy as np
import random
from db.orm.tables import *


class LoadRandomTeacherScheduleTask:
	def __init__(self, db):
		self.db = db

	def load_teachers(self):
		return pd.read_sql('select * from verif_teacher', con=self.db.engine)

	def load_to_db(self):
		self.create_schedule().to_sql('teacher_wish_schedule', con=self.db.engine, if_exists='append', index=False)

	def create_schedule(self):
		df_teachers = self.load_teachers()
		teachers_id = tuple(df_teachers.teacher_id.values)
		df_cards = pd.read_sql(f'select * from card where teacher_id in {teachers_id}', con=self.db.engine)
		df_cards = self.multiply_amount_time(df_cards)
		df_cards = self.prepare_data_db(df_cards, teachers_id, df_teachers)

		return df_cards
	
	def multiply_amount_time(self, df_cards):

		return df_cards.loc[df_cards.index.repeat(df_cards.amount_time)].reset_index(drop=True)

	def prepare_data_db(self, df_cards, teachers_id, df_teachers):
		pair_days = pd.DataFrame([(i,j) for j in range(1,6)for i in range(1,13)], columns=['day','para'])
		
		for t in teachers_id:
			mask = df_cards.teacher_id==t

			sample_day_pair = pair_days.sample(len(df_cards[mask]))
			df_cards.loc[mask,['days_id','pairs_id']] = [tuple(x) for x in sample_day_pair.to_numpy()]
			df_cards.loc[mask,['tchr_secret_key']] =  [df_teachers[df_teachers.teacher_id==t].tchr_secret_key for _ in range(len(df_cards[mask]))]
		
		df_cards.drop(columns=['group_id','teacher_id','lesson_id','amount_time'], inplace=True)
		
		return df_cards