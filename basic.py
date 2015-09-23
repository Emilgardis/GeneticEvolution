"""
Sum of list of len y is x.
The way to get this is to mutate and evolve.
Based on http://lethain.com/genetic-algorithms-cool-name-damn-simple/
"""
from random import randint, random, shuffle, sample


def make_individual(length, minmax):
    return [randint(minmax[0], minmax[1]) for _ in range(length)]

def get_population(count, length, minmax=(0, 2**7)):
    return [make_individual(length, minmax) for _ in range(count)]

def fitness(individual, target):
    return abs(target-sum(individual))

def grade(population, target):
    whole = sum(fitness(ind, target) for ind in population)
    return whole/len(population)

def hamming_distance(l1, l2):
    if len(s1) != len(s2):
        return ValueError("Undefined for sequences of unequal length")
    return sum(i1 != i2 for i1, i2 in zip(l1, l2))

def evolve(population, target, ind_len, minmax,
           retain=0.2,
           random_select=0.05,
           mutate=0.01,
           ):
    graded = sorted(population, key=lambda ind: fitness(ind, target))
    retain_amount = int(len(graded)*retain)
    print("Graded: {}".format(graded))
    parents = graded[:retain_amount]
    print("Parents: {}".format(parents))
    for ind in parents:
        if mutate > random():
            ind[randint(0, ind_len-1)] = randint(*minmax)
    print("Parents + rand: {}".format(parents))
    shuffle(parents) # In place shuffle
    par_len = len(parents)
    needed = len(population) - par_len # How many children are needed
    children = []
    partners = parents[:]
    while len(children) < needed:
        male, female = sample(parents, 2)
        dist = randint(1, ind_len-1 if ind_len > 2 else 2)
        child = [male[dist:] + female[:dist], female[dist:] + male[:dist]]
        children.extend(child)
    parents.extend(children)
    return parents
