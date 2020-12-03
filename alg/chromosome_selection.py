import numpy as np
from alg.fitness_function import FitnessFunction

class ChromosomeSelection(FitnessFunction):

	def __init__(self, chromosomes, clc_obj, swc_obj, twc_obj):

		self.n_chromo = len(chromosomes)
		super().__init__(clc_obj, swc_obj, twc_obj)
		
		self.chromosomes = {
			ind: [chromo, self.sumUpChromosome(chromo)]
			for ind, chromo in enumerate(chromosomes)
		}


	def wfold_tour(self, w = 5):

		keys = np.random.choice(self.n_chromo, w, replace = False)
		score_values = [(self.chromosomes[key][1], key) for key in keys]
		score_values.sort(reverse = True)

		parent1_key = score_values[0][1]
		parent2_key = np.random.choice(self.n_chromo, 1)[0]

		parent1 = self.chromosomes[parent1_key][0]
		parent2 = self.chromosomes[parent2_key][0]

		return parent1, parent2