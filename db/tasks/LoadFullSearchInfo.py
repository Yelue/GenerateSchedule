import pandas as pd


class LoadFullSearchInfo:
	def __init__(self, db, user_status, ids):
		self.db = db
		self.user_status = user_status
		self.ids = tuple(map(lambda x: x[0], ids))

	def find_card(self):
		df = pd.read_sql(f"select class_id,card_id,pairs_id,days_id from class where class_id in {self.ids}", con=self.db.engine)

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
		
		df.rename(columns={'class_id':'id'}, inplace=True)
		df = self.format_lecture(df) if self.user_status=='teacher' else df
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
	
	def format_lecture(self,df):
		lectures = df[['pairs_id','days_id']][df[['pairs_id','days_id']].duplicated()].drop_duplicates(keep='first')
		lectures = [list(i) for i in lectures.values]
		data = {}
		for i in lectures:
			data[tuple(i)] = ', '.join(list(df[(df.pairs_id==i[0])&(df.days_id==i[1])]['group_name'].values))
		df.drop_duplicates(subset=['pairs_id', 'days_id'], keep='first', inplace=True)
		for i in data.keys():	
			df.loc[(df.pairs_id==i[0])&(df.days_id==i[1]),'group_name'] = data[i]

		return df

	def create_schedule(self):
		df = self.find_card()
		df = self.full_info(df)
		df = self.format_data(df)
		return df
