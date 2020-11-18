import pandas as pd


class LoadFullSearchInfo:
	def __init__(self, db, user_status, ids):
		self.db = db
		self.user_status = user_status
		# self.user_key = user_key
		self.ids = tuple(map(lambda x: x[0], ids))

	def find_card(self):
		if self.user_status=='student':
			table = 'student_wish_schedule'
			self.column_key = 'st_schedule_id'
		else:
			table = 'teacher_wish_schedule'
			self.column_key = 'tchr_schedule_id'

		df = pd.read_sql(f"select {self.column_key},card_id,pairs_id,days_id from {table} where {self.column_key} in {self.ids}", con=self.db.engine)


		return df

	def full_info(self, df):
		ids = tuple(df.card_id.values)
		card = pd.read_sql(f'select * from card where card_id in {ids}', con=self.db.engine)
		df = df.merge(card, how='inner', on='card_id')

		#lesson
		lesson = pd.read_sql('select * from lesson', con=self.db.engine)
		df = df.merge(lesson, how='inner', on='lesson_id').drop(columns=['lesson_id'])
		del lesson
		#group
		group = pd.read_sql('select group_id, group_name from groups', con=self.db.engine)
		df = df.merge(group, how='inner', on='group_id').drop(columns=['group_id'])
		del group
		#teacher
		teacher = pd.read_sql('select * from teacher', con=self.db.engine)
		df = df.merge(teacher, how='inner', on='teacher_id').drop(columns=['teacher_id','teacher_degree'])
		del teacher
		# return df.drop(columns=[self.column_key,'card_id', 'lesson_id', 'lesson_long_name'])
		return df.drop(columns=['card_id','amount_time'])
	def format_data(self, df):
		df.loc[df.lesson_type=='None','lesson_type'] = ''
		
		df.rename(columns={'st_schedule_id':'id','tchr_schedule_id':'id'}, inplace=True)

		# (df.days_id==j)&(df.pairs_id==i)
		# print({'lesson%s'%i: [df[(df.days_id==j)&(df.pairs_id==i)].to_dict('r') for j in range(1,7)] for i in range(1,6)})
		data = {
				'week1':{
					'lesson%s'%i: [df[(df.days_id==j)&(df.pairs_id==i)].to_dict('records') for j in range(1,7)] for i in range(1,6)
				},
				'week2':{
					'lesson%s'%i: [df[(df.days_id==j)&(df.pairs_id==i)].to_dict('records') for j in range(7,13)] for i in range(1,6)
				}
		}
		for week in data.keys():
			for lesson in data[week].keys():
				for k, cell in enumerate(data[week][lesson]):

					if not cell:
						data[week][lesson][k] = 0


		return data
	def create_schedule(self):
		df = self.find_card()
		df = self.full_info(df)
		df = self.format_data(df)
		return df
