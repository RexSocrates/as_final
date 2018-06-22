
#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:fonttian 
@file: Overview.py
@time: 2017/10/15 
"""

# Types思考你問題的類型   最小值？最大值？
from deap import base, creator

#deap.creator.create（name，base [，attribute [，... ] ] ）#class deap.base.Fitness（[ values ] ）
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
# weights : 1.0求最大值,-1.0 求最小值 ; (1.0,-1.0,)求第一個參數的最大值,求第二個參數的最小值
creator.create("Individual", list, fitness=creator.FitnessMax)  #創造個體模塊

# Initialization
import random
from deap import tools

IND_SIZE = 10 # 基因長度
toolbox = base.Toolbox()
#register(alias, method[, argument[, ...]])
toolbox.register("attribute", random.random)
# 調用randon.random為每一個基因編碼編碼創建 隨機初始值 也就是範圍[0,1]
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attribute, n=IND_SIZE)#建立染色體模板
#deap.tools.initRepeat(container, func, n)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)#建立多個染色體數模板


# Operators
# difine evaluate function
# Note that a comma is a must
def evaluate(individual): #目標函數值
    return sum(individual),

# use tools in deap to creat our application
toolbox.register("mate", tools.cxTwoPoint) # mate:交叉
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.1) # mutate : 變異
toolbox.register("select", tools.selTournament, tournsize=3) # select : 選擇保留的最佳個體
toolbox.register("evaluate", evaluate)  # commit our evaluate


# Algorithms
def main():
    pop = toolbox.population(n=50)#染色體個數
    print(pop)
    CXPB, MUTPB, NGEN = 0.5, 0.2, 40#交配率,突變率,迭代數
    '''
    # CXPB  is the probability with which two individuals
    #       are crossed
    #
    # MUTPB is the probability for mutating an individual
    #
    # NGEN  is the number of generations for which the
    #       evolution runs
    '''
    # Evaluate the entire population
    fitnesses = map(toolbox.evaluate, pop)
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
        #print(ind.fitness.values )
    print("  Evaluated %i individuals" % len(pop))
    print("-- Iterative %i times --" % NGEN)

    for g in range(NGEN):
        #if g % 1 == 0:
            #print("-- Generation %i --" % g)
        # Select the next generation individuals選擇子代
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))
        # Change map to list,The documentation on the official website is wrong
        # Apply crossover and mutation on the offspring子代的基因交叉、變異產生新的子代
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness重新評估個體
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]#
        fitnesses = map(toolbox.evaluate, invalid_ind)

        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
            print(ind.fitness.values)

        # The population is entirely replaced by the offspring
        pop[:] = offspring

    print("-- End of (successful) evolution --")

    best_ind = tools.selBest(pop, 1)[0]

    return best_ind, best_ind.fitness.values  # return the result:Last individual,The Return of Evaluate function


if __name__ == "__main__":
    # t1 = time.clock()
    best_ind, best_ind.fitness.values = main()
    # print(pop, best_ind, best_ind.fitness.values)
    # print("pop",pop)
    print("best_ind",best_ind)
    print("best_ind.fitness.values",best_ind.fitness.values)

    # t2 = time.clock()

    # print(t2-t1)
