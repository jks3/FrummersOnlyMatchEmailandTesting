import sys
import scipy.optimize as sc
import scipy as scm
import numpy as np
import platypus
import itertools

class Person:
    def __init__(self, my_attributes, my_weights):
        self.my_attributes = np.array(my_attributes)
        self.my_weights = np.array(my_weights)
        self.my_scores = dict()

    def get_my_score(self, your_attributes):
        return np.dot(self.my_weights, np.array(your_attributes))


class Match_Tuple:
    match_tuples = dict()

    def __init__(self, person_a, person_b):
        self.match_tuples[frozenset({person_a, person_b})] = frozenset(
            {person_a.my_scores[person_b], person_b.my_scores[person_a]})


#x = Person([3, 10, 8], [.6, .2, .2])
#y = Person([9, 4, 2], [.5, .3, .2])

boys = []
girls = []

for i in range(5):

    boy_attributes = np.random.randint(low = 0, high = 10, size = 5)

    boy_weights = np.random.randint(low = 0, high = 10, size = 5)
    boy_weights = boy_weights/boy_weights.sum()

    girl_attributes = np.random.randint(low=0, high=10, size=5)

    girl_weights = np.random.randint(low=0, high=10, size=5)
    girl_weights = girl_weights / girl_weights.sum()

    boys.append(Person(boy_attributes, boy_weights))

    girls.append(Person(girl_attributes, girl_weights))

for i in range(len(boys)):
    for j in range(len(girls)):
        boys[i].my_scores[girls[j]] = boys[i].get_my_score(girls[j].my_attributes)

        girls[j].my_scores[boys[i]] = girls[j].get_my_score(boys[i].my_attributes)

        a = Match_Tuple(boys[i], girls[j])

#print(Match_Tuple.match_tuples)

print(Match_Tuple.match_tuples[frozenset({boys[0], girls[0]})])

all_combinations = []

list1_permutations = itertools.permutations(boys, len(girls))

for each_permutation in list1_permutations:
    zipped = zip(each_permutation, girls)
    all_combinations.append(list(zipped))

print(all_combinations)

#truth = []

#for combo in all_combinations:
#    for i in range(len(combo)):

#        truth_i = []

#        j_list = list(range(len(combo)))

#        j_list.remove(i)

#        for j in j_list:
#            if set(combo[i]).isdisjoint(set(combo[j])):
#                truth_i.append(True)
#            else:
#                truth_i.append(False)

#        if not (False in truth_i):
#            truth.append(True)
#        else:
#            truth.append(False)
#print(not (False in truth))

def belegundu(vars):
    x = vars[0]
    y = vars[1]
    return [-2*x + y, 2*x + y], [-x + y - 1, x + y - 7]

problem = platypus.Problem(2, 2, 2)
problem.types[:] = [platypus.Real(0, 5), platypus.Real(0, 3)]
problem.constraints[:] = "<=0"
problem.function = belegundu

algorithm = platypus.NSGAII(problem)
algorithm.run(10000)