import numpy as np
import pandas as pd

from alg.student_wishes import SWishesConnector
from alg.teacher_wishes import TWishesConnector
from alg.collection_cards import CollectionCards


class Priority:

	priorityCourses = {

		1: 1,
		2: 2,
		3: 3,
		4: 4,
		5: 5,
		6: 6,
	}

	priorityTeachers = {

		'асистент': 1,
		'викладач': 2, 
		'старший викладач': 2.5,
		'доцент': 3,
		'професор': 4,
		'завідувач кафедри': 5,
		'декан': 6,
		'проректор': 7,
		'ректор': 8 
	
	}



class FitnessFunction(Priority):

	def __init__(self, clc_obj, swc_obj, twc_obj):
		
		self.clc = clc_obj
		self.swc = swc_obj
		self.twc = twc_obj


	def sumUpTeachers(self, chromosome, teacher_id, card_id):
		
		teacher = self.twc.get_teacherByTeacherId(teacher_id)
		score = FitnessFunction.priorityTeachers[teacher.teacher_degree] *\
				np.sum(chromosome.teachers[teacher_id] * teacher.cards[card_id]) *\
				np.sum(chromosome.teachers[teacher_id] * teacher.work_time)

		return score


	def sumUpGroups(self, chromosome, group_id, card_id):
		
		group = self.swc.get_groupByGroupId(group_id)
		score = FitnessFunction.priorityCourses[group.group_course] *\
				np.sum(chromosome.groups[group_id] * group.cards[card_id]) *\
				np.sum(chromosome.groups[group_id] * group.work_time)

		return score


	def sumUpChromosome(self, chromosome):

		max_score = self.swc.wdc_shape[2]
		pWindows = np.zeros(self.swc.wdc_shape)
		for i in range(max_score):
			pWindows[:,:,i] = max_score - i

		pWindows[:,:,0] = pWindows[:,:,1]
		pWindows /= np.sum(pWindows)
		# the same priority for first and second lesson
		
		chromosome_score = 0
		for lesson in chromosome.lessons:
			for card_id in lesson.cards:

				card = self.clc.get_cardByCardId(card_id)
				group_id, teacher_id = card.group_id, card.teacher_id

				scoreG = self.sumUpGroups(chromosome, group_id, card_id)
				scoreT = self.sumUpTeachers(chromosome, teacher_id, card_id)

				chromosome_score += (scoreT + scoreG)
				chromosome_score += np.sum(chromosome.groups[group_id] * pWindows)

		return chromosome_score