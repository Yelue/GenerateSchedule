import pandas as pd 


class LoadFullInfo:
	def __init__(self, db, user_status, user_key):
		self.db = db
		self.user_status = user_status
		self.user_key = user_key

	def find_card(self):
		if self.user_status=='student':
			table = 'student_wish_schedule'
			self.column_key = 'st_secret_key'
		else:
			table = 'teacher_wish_schedule'
			self.column_key = 'tchr_secret_key'
		
		df = pd.read_sql(f"select * from {table} where {self.column_key} = '{self.user_key}'", con=self.db.engine)
		return df

	def full_info(self, df):
		card = pd.read_sql('select lesson_id, card_id from card', con=self.db.engine)
		df = df.merge(card, how='inner', on='card_id')
		
		#lesson
		lesson = pd.read_sql('select * from lesson', con=self.db.engine)
		df = df.merge(lesson, how='inner', on='lesson_id')
		return df.drop(columns=[self.column_key,'card_id', 'lesson_id', 'lesson_long_name']) 

	def format_data(self, df):
		df.loc[df.lesson_type=='None','lesson_type'] = ''
		df['name'] = df['lesson_short_name']+ ' ' +df['lesson_type']
		df.rename(columns={'st_schedule_id':'id','tchr_schedule_id':'id'}, inplace=True)
		df.drop(columns=['lesson_short_name','lesson_type'],inplace=True)

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