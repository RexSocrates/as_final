from deap import base, creator, tools

creator.create("Fitness_mini", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

import random
from deap import tools

# initialize population size
IND_SIZE = 10 
toolbox = base.Toolbox()

toolbox.register("attribute", random.random)

toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attribute, n=IND_SIZE)

toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# fitness function
def evaluate(individual): 
    return sum(individual),

# choose the crossover function as uniform
toolbox.register("mate", tools.cxUniform) 
# mutation function
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.1) 
# selection of next generation
toolbox.register("select", tools.selBest, tournsize=3) 
# evaluate the fitness value of the chromosome
toolbox.register("evaluate", evaluate)

def main():
    pop = toolbox.population(n=50)
    # print(pop)

    # crossover rate
    CXPB = 0.5

    # mutation rate
    MUTPB = 0.2

    # number of generations
    NGEN = 1000

    fitness = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitness) :
    	ind.fitness.value = fit
    	print(fit)

    fits = [ind.fitness.value[0] for ind in pop]

    generations = 0

    while generations < NGEN :
    	generations = generations + 1
    	print("Generation %i" % generations)

    	# select the next generation
    	offspring = toolbox.select(pop, len(pop))
    	# Clone the selected individuals
    	offspring = list(map(toolbox.clone, offspring))

    	for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values







