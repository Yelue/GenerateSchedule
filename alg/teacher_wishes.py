import numpy as np
import pandas as pd 

from alg.professor import Professor
from db.orm.tables import (Department, Groups, Card, Teacher,
						Teacher_Wish_Schedule, Verif_Teachers)



class TWishesConnector:

	def __init__(self, facultyID, session_obj, 
				 n_weeks = 2, n_days = 6, n_classes = 5):

		self.teachers = {}
		self.wdc_shape = (n_weeks, n_days, n_classes)

		self.session = session_obj
		self.facultyID = facultyID

		self.create_teachers()


	def get_allTeacherWishes(self):

		data = pd.read_sql(self.session.query(Teacher_Wish_Schedule, Teacher.teacher_id, Teacher.teacher_degree).\
			select_from(Department).join(Groups).join(Card).join(Teacher_Wish_Schedule).join(Verif_Teachers).\
			join(Teacher).filter(Department.faculty_id == self.facultyID).statement, self.session.bind)
		
		return data


	def create_teachers(self):
		
		data = self.get_allTeacherWishes()
		for teacher_id, frame1 in data.groupby('teacher_id'):
			
			ind = frame1.index
			teacher_degree = frame1.loc[ind[0], 'teacher_degree']
			new_teacher = Professor(teacher_id, teacher_degree)
			
			work_time = np.zeros(self.wdc_shape) 
			for card_id, frame2 in frame1.groupby('card_id'):

				time_table = np.zeros(self.wdc_shape)
				for i in frame2.index:

					week = (frame2.loc[i, 'days_id'] - 1) // 6
					day  = (frame2.loc[i, 'days_id'] - 1) % 6
					pair = (frame2.loc[i, 'pairs_id']- 1)

					time_table[week, day, pair] += 1
					work_time[week, day, pair] += 1

				new_teacher.cards[card_id] = time_table / np.sum(time_table)

			new_teacher.work_time = work_time / np.sum(work_time)
			self.teachers[teacher_id] = new_teacher


	def get_teacherByTeacherId(self, teacher_id):
		return self.teachers[teacher_id]
