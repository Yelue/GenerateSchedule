import numpy as np 


class TimeTable:
	
	def __init__(self, rooms, n_weeks = 2, 
				 n_days = 6, n_classes = 5):

		self.timeTable = { 
			room: np.zeros((n_weeks, n_days, n_classes)) for room in rooms }


	def get_wdcByLessonNum(self, value):

		for room in self.timeTable:
			wdc = np.argwhere(self.timeTable[room] == value)

			if wdc.size != 0:
				return room, list(map(tuple, wdc))[0]

