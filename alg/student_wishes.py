import numpy as np
import pandas as pd

from alg.group import Group
from db.orm.tables import (Department, Groups, 
						Verif_Students, Student_Wish_Schedule)


class SWishesConnector:
	
	def __init__(self, facultyID, session_obj,
		n_weeks = 2, n_days = 6, n_classes = 5):

		self.groups = {}
		self.wdc_shape = (n_weeks, n_days, n_classes)

		self.session = session_obj
		self.facultyID = facultyID

		self.create_groups()


	def get_allStudentWishes(self):

		data = pd.read_sql(self.session.query(Student_Wish_Schedule, Groups.group_id, Groups.group_course).select_from(Department).\
						   join(Groups).join(Verif_Students).join(Student_Wish_Schedule).filter(Department.faculty_id == self.facultyID).statement, self.session.bind)
		return data


	def create_groups(self):
		
		data = self.get_allStudentWishes()
		for group_id, frame1 in data.groupby('group_id'):
			
			ind = frame1.index
			group_course = frame1.loc[ind[0], 'group_course']
			
			new_group = Group(group_id, group_course)
			work_time = np.zeros(self.wdc_shape) 
			for card_id, frame2 in frame1.groupby('card_id'):

				time_table = np.zeros(self.wdc_shape)
				for i in frame2.index:

					week = (frame2.loc[i, 'days_id'] - 1) // 6
					day  = (frame2.loc[i, 'days_id'] - 1) % 6
					pair = (frame2.loc[i, 'pairs_id']- 1)

					time_table[week, day, pair] += 1
					work_time[week, day, pair] += 1

				new_group.cards[card_id] = time_table / np.sum(time_table)

			new_group.work_time = work_time / np.sum(work_time)
			self.groups[group_id] = new_group


	def get_groupByGroupId(self, group_id):
		return self.groups[group_id]
