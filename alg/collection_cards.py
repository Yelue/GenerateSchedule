import numpy as np
import pandas as pd
from db.orm.tables import Department, Groups, Card


class LessonCard:
	
	def __init__(self, card_id, 
		group_id, teacher_id):

		self.card_id = card_id
		self.group_id = group_id
		self.teacher_id = teacher_id



class CollectionCards:

	def __init__(self, facultyID, session_obj):
		
		self.cards = {}
		self.session = session_obj
		self.facultyID = facultyID
		self.create_cards()


	def get_allFacultyCard(self):

		data = pd.read_sql(self.session.query(Card).select_from(Department).\
			join(Groups).join(Card).filter(Department.faculty_id == self.facultyID).statement, self.session.bind)

		return data


	def create_cards(self):

		data = self.get_allFacultyCard()
		for ind in data.index:

			key = data.loc[ind, 'card_id']
			self.cards[key] = LessonCard(
					key,
					data.loc[ind, 'group_id'],
					data.loc[ind, 'teacher_id']
				)


	def get_cardByCardId(self, card_id):
		return self.cards[card_id]