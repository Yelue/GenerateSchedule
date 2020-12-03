import numpy as np
from alg.chromosome import Chromosome 


class ChromosomeCrossover:

	def fill_data(self, chromosome, room, 
				  wdc, teacherID, groupIDs, uniqueNumber):

		chromosome.teachers[teacherID][wdc] = 1
		chromosome.timeTable[room][wdc] = uniqueNumber

		for group_id in groupIDs:
			chromosome.groups[group_id][wdc] = 1


	def crossover(self, chromosome1, chromosome2):

		child = Chromosome(
			chromosome1.rooms, 
			chromosome2.groupIDs, 
			chromosome1.teacherIDs,
			chromosome2.collection_cards, 
			*chromosome1.wdc_shape
		)

		child.lessons = chromosome2.lessons
		for lesson in child.lessons:

			cardsL = lesson.cards
			teacherID, groupIDs = child.get_GTIndexes(cardsL)

			chromo1_room, chromo1_wdc = chromosome1.get_wdcByLessonNum(lesson.unNum)
			chromo2_room, chromo2_wdc = chromosome2.get_wdcByLessonNum(lesson.unNum)

			dice = np.random.randint(0, 2, 1)
			if dice == 0 and child.check_place_time(teacherID, groupIDs, chromo1_room, chromo1_wdc):
				self.fill_data(child, chromo1_room, chromo1_wdc, teacherID, groupIDs, lesson.unNum)

			elif dice == 1 and child.check_place_time(teacherID, groupIDs, chromo2_room, chromo2_wdc):
				self.fill_data(child, chromo2_room, chromo2_wdc, teacherID, groupIDs, lesson.unNum)

			else:

				room, wdc = child.choice_place_time(teacherID, groupIDs)
				self.fill_data(child, room, wdc, teacherID, groupIDs, lesson.unNum)

		return child