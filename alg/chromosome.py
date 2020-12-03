import numpy as np
import pandas as pd

from alg.time_table import TimeTable
from db.orm.tables import (Teacher, Groups, Card,
						Lesson, Department)


class UniqueLesson:
	
	def __init__(self, uniqueNumber, cards):
		self.cards = cards
		self.unNum = uniqueNumber


class Chromosome(TimeTable):

	def __init__(self, rooms, groupIDs, teacherIDs, cc_obj,
				 n_weeks = 2, n_days = 6, n_classes = 5):

		self.lessons = []
		self.rooms = rooms
		self.groupIDs = groupIDs
		self.teacherIDs = teacherIDs
		self.wdc_shape = (n_weeks, n_days, n_classes)
		
		self.collection_cards = cc_obj
		super().__init__(rooms, n_weeks, 
						 n_days, n_classes)

		self.groups = {
			group_id: np.zeros((n_weeks, n_days, n_classes)) 
			for group_id in groupIDs
		}


		self.teachers = {
			teacher_id: np.zeros((n_weeks, n_days,  n_classes))
			for teacher_id in teacherIDs
		}


	def get_GTIndexes(self, cardsL):

		groupIDs = []
		for card_id in cardsL:
			card = self.collection_cards.get_cardByCardId(card_id)

			teacherID = card.teacher_id
			groupIDs.append(card.group_id)

		return teacherID, groupIDs


	def check_place_time(self, teacherID, groupIDs, room, wdc):

		occupationMatrix = self.teachers[teacherID].copy()
		for group_id in groupIDs:
			occupationMatrix += self.groups[group_id]

		occupationMatrix += self.timeTable[room]
		value = occupationMatrix[wdc]
		
		return True if value == 0 else False


	def choice_place_time(self, teacherID, groupIDs):

		occupationMatrix = self.teachers[teacherID].copy()
		for group_id in groupIDs:
			occupationMatrix += self.groups[group_id]

		np.random.shuffle(self.rooms)
		for room in self.rooms:
			wdc = np.argwhere((occupationMatrix + self.timeTable[room]) == 0)
			
			if wdc.size:
				ind = np.random.randint(0, wdc.shape[0], 1)[0]
				return room, tuple(wdc[ind])

		raise 'There is not any free room'		


	def create_chromosome(self, dataL, dataP):

		uniqueNumber = 0
		for group, frame in dataL.groupby('lesson_id'):

			cardsL = frame.card_id.to_numpy()
			teacherID, groupIDs = self.get_GTIndexes(cardsL)

			for _ in range(pd.to_numeric(frame.amount_time.iloc[0])):

				uniqueNumber += 1
				room, wdc = self.choice_place_time(teacherID, groupIDs)

				self.teachers[teacherID][wdc] = 1
				self.timeTable[room][wdc] = uniqueNumber
				self.lessons.append(UniqueLesson(uniqueNumber, cardsL))

				for group_id in groupIDs:
					self.groups[group_id][wdc] = 1
				

		for ind in dataP.index:
			
			cardsL = np.array([dataP.loc[ind, 'card_id']])
			teacherID, groupIDs = self.get_GTIndexes(cardsL)
			for _ in range(pd.to_numeric(dataP.amount_time.iloc[ind])):

				uniqueNumber += 1
				room, wdc = self.choice_place_time(teacherID, groupIDs)

				self.teachers[teacherID][wdc] = 1
				self.timeTable[room][wdc] = uniqueNumber
				self.lessons.append(UniqueLesson(uniqueNumber, cardsL))

				for group_id in groupIDs:
					self.groups[group_id][wdc] = 1