from deap import base, creator


creator.create("FitnessMax", base.Fitness, weights=(1.0,))

creator.create("Individual", list, fitness=creator.FitnessMax)


import random
from deap import tools

IND_SIZE = 10 
toolbox = base.Toolbox()

toolbox.register("attribute", random.random)

toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attribute, n=IND_SIZE)

toolbox.register("population", tools.initRepeat, list, toolbox.individual)





def evaluate(individual): 
    return sum(individual),


toolbox.register("mate", tools.cxTwoPoint) 
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.1) 
toolbox.register("select", tools.selTournament, tournsize=3) 
toolbox.register("evaluate", evaluate)  



def main():
    pop = toolbox.population(n=50)
    print(pop)
    CXPB, MUTPB, NGEN = 0.5, 0.2, 40
    
    fitnesses = map(toolbox.evaluate, pop)
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
        #print(ind.fitness.values )
    print("  Evaluated %i individuals" % len(pop))
    print("-- Iterative %i times --" % NGEN)

    for g in range(NGEN):
        offspring = toolbox.select(pop, len(pop))
        
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

        
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]#
        fitnesses = map(toolbox.evaluate, invalid_ind)

        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
            print(ind.fitness.values)

        
        pop[:] = offspring

    print("-- End of (successful) evolution --")

    best_ind = tools.selBest(pop, 1)[0]

    return best_ind, best_ind.fitness.values


if __name__ == "__main__":
    
    best_ind, best_ind.fitness.values = main()
    
    
    print("best_ind",best_ind)
    print("best_ind.fitness.values",best_ind.fitness.values)

    