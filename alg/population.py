import pandas as pd
from sqlalchemy import and_

from alg.chromosome import Chromosome
from alg.student_wishes import SWishesConnector
from alg.teacher_wishes import TWishesConnector
from alg.collection_cards import CollectionCards

from db.orm.tables import (Teacher, Groups, Card,
						Lesson, Department)


class Population:

	def __init__(self, rooms, n_chromo, facultyID, session_obj, 
				 n_weeks = 2, n_days = 6, n_classes = 5):

		self.rooms = rooms
		self.chromosomes = []
		self.n_chromo = n_chromo

		self.facultyID = facultyID
		self.session = session_obj
		self.wdc_shape = (n_weeks, n_days, n_classes)

		self.clc = CollectionCards(self.facultyID, self.session)
		self.swc = SWishesConnector(self.facultyID, self.session, *self.wdc_shape)
		self.twc = TWishesConnector(self.facultyID, self.session, *self.wdc_shape)


	def get_allFacultyLecture(self):

		dataL = pd.read_sql(self.session.query(Card.card_id, Lesson.lesson_id, Card.amount_time).select_from(Department).\
				join(Groups).join(Card).join(Lesson).filter(and_(Department.faculty_id == self.facultyID, 
					Lesson.lesson_type == 'Лек')).statement, self.session.bind)
		
		return dataL


	def get_allFacultyPractice(self):

		dataP = pd.read_sql(self.session.query(Card.card_id, Lesson.lesson_id, Card.amount_time).select_from(Department).\
				join(Groups).join(Card).join(Lesson).filter(and_(Department.faculty_id == self.facultyID, 
					Lesson.lesson_type != 'Лек')).statement, self.session.bind)
		
		return dataP


	def get_allTeachersID(self):
		return list(self.twc.teachers.keys())


	def get_allGroupsID(self):
		return list(self.swc.groups.keys())


	def create_chromosomes(self):

		dataL = self.get_allFacultyLecture()
		dataP = self.get_allFacultyPractice()

		groupIDs = self.get_allGroupsID()
		teacherIDs = self.get_allTeachersID()

		for _ in range(self.n_chromo):

			chromo = Chromosome(self.rooms, groupIDs, 
								teacherIDs, self.clc, *self.wdc_shape)
			
			chromo.create_chromosome(dataL, dataP)
			self.chromosomes.append(chromo)