import numpy as np


class ChromosomeMutation:

	def mutation(self, chromosome):

		n_lessons = len(chromosome.lessons)
		n_mutation = np.random.randint(1, int(0.1 * n_lessons), 1)[0]

		indexes = np.random.choice(n_lessons, n_mutation, replace = False)
		for index in indexes:

			cardsL = chromosome.lessons[index].cards
			teacherID, groupIDs = chromosome.get_GTIndexes(cardsL)

			new_room, new_wdc = chromosome.choice_place_time(teacherID, groupIDs)
			old_room, old_wsc = chromosome.get_wdcByLessonNum(chromosome.lessons[index].unNum)

			chromosome.teachers[teacherID][new_wdc], chromosome.teachers[teacherID][old_wsc] =\
													 chromosome.teachers[teacherID][old_wsc], chromosome.teachers[teacherID][new_wdc]
			
			chromosome.timeTable[new_room][new_wdc], chromosome.timeTable[old_room][old_wsc] =\
													 chromosome.timeTable[old_room][old_wsc], chromosome.timeTable[new_room][new_wdc]

			for group_id in groupIDs:
				chromosome.groups[group_id][new_wdc], chromosome.groups[group_id][old_wsc] =\
				 									  chromosome.groups[group_id][old_wsc], chromosome.groups[group_id][new_wdc]

		return chromosome



