import numpy as np
from alg.chromosome_mutation import ChromosomeMutation
from alg.chromosome_selection import ChromosomeSelection
from alg.chromosome_crossover import ChromosomeCrossover


class GeneticAlgorithm(ChromosomeSelection, 
	ChromosomeCrossover, ChromosomeMutation):

	def __init__(self, chromosomes, clc_obj, swc_obj, twc_obj):
		super().__init__(chromosomes, clc_obj, swc_obj, twc_obj)

		self.percent_mutation  = 0.15
		self.percent_crossover = 0.75


	def update_population(self, new_chromosomes):
		
		chromosomes = [value[0] for value in self.chromosomes.values()]
		chromosomes.extend(new_chromosomes)
		
		score_chromosomes = [(chromo, self.sumUpChromosome(chromo)) 
							  for chromo in chromosomes]

		score_chromosomes.sort(key = lambda x: x[1], reverse = True)
		self.chromosomes = { ind: [value[0], value[1]]
			for ind, value in enumerate(score_chromosomes[:self.n_chromo])
		}


	def fit(self, n_iter = 5):
		
		for iter in range(n_iter):

			new_chromosomes = []
			for _ in range(int(self.n_chromo * self.percent_crossover)):

				parent1, parent2 = self.wfold_tour()
				child = self.crossover(parent1, parent2)

				number = np.random.uniform(0, 1, 1)[0]
				if number < self.percent_mutation:
					child = self.mutation(child)

				new_chromosomes.append(child)

			self.update_population(new_chromosomes)

			print('\nPopulation: {}'.format(iter))
			for key in range(5):
				print('{} Score: {}'.format(key, self.chromosomes[key][1]))
