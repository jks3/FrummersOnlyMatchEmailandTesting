import sys

import scipy
import scipy as scipy
import scipy.optimize as sc
import scipy as scm
import numpy as np
import platypus.core as ptcore
import platypus.types as pttypes
import platypus.algorithms as ptalgo
import itertools
import statistics

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

for i in range(100):

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

        if boys[i].my_scores[girls[j]] == girls[j].my_scores[boys[i]]:
            girls[j].my_scores[boys[i]] = girls[j].my_scores[boys[i]] + .1

        a = Match_Tuple(boys[i], girls[j])

#print(Match_Tuple.match_tuples)

w, h = 100, 100

payoff_mat = [[0 for x in range(w)] for y in range(h)]
distance_mat = [[0 for x in range(w)] for y in range(h)]


#print(list(Match_Tuple.match_tuples[frozenset({boys[400], girls[400]})])[1])

#print(float(-sys.maxsize))

for i in range(len(boys)):
    for j in range(len(girls)):
        #if list(Match_Tuple.match_tuples[frozenset({boys[i], girls[j]})])[0] >= 2 and \
        #    list(Match_Tuple.match_tuples[frozenset({boys[i], girls[j]})])[1] >= 2:
            payoff_mat[i][j] = float(list(Match_Tuple.match_tuples[frozenset({boys[i], girls[j]})])[0])
            + float(list(Match_Tuple.match_tuples[frozenset({boys[i], girls[j]})])[1]) \
            - abs(float(list(Match_Tuple.match_tuples[frozenset({boys[i], girls[j]})])[0])
            - float(list(Match_Tuple.match_tuples[frozenset({boys[i], girls[j]})])[1]))

            distance_mat[i][j] = abs(float(list(Match_Tuple.match_tuples[frozenset({boys[i], girls[j]})])[0])
            - float(list(Match_Tuple.match_tuples[frozenset({boys[i], girls[j]})])[1]))
        #else:
        #    payoff_mat[i][j] = -sys.maxsize

payoff_flat = []
distance_flat = []

for i in range(len(payoff_mat)):
    for j in range(len(payoff_mat[i])):
        payoff_flat.append(payoff_mat[i][j])
        distance_flat.append(distance_mat[i][j])

payoff_stdev = statistics.stdev(payoff_flat)
payoff_mean = statistics.mean(payoff_flat)

distance_stdev = statistics.stdev(distance_flat)
distance_mean = statistics.mean(distance_flat)

#print(payoff_stdev)

#print(payoff_mean)

#print(distance_stdev)

#print(distance_mean)

#print(payoff_flat == distance_flat)

for i in range(len(payoff_mat)):
    for j in range(len(payoff_mat[i])):
        if payoff_mat[i][j] < payoff_mean or distance_mat[i][j] > distance_mean + distance_stdev:
            payoff_mat[i][j] = -sys.maxsize

#print(payoff_mat[0])

dom, rang = scipy.optimize.linear_sum_assignment(payoff_mat, maximize = True)

opt_payoffs_vec = []

for i in range(len(dom)):
    opt_payoffs_vec.append(payoff_mat[dom[i]][rang[i]])

print(opt_payoffs_vec)

print(opt_payoffs_vec.count(-sys.maxsize)/len(opt_payoffs_vec))

#all_combinations = []

#list1_permutations = itertools.permutations(boys, len(girls))

#for each_permutation in list1_permutations:
#    zipped = zip(each_permutation, girls)
#    all_combinations.append(list(zipped))

#print(all_combinations)

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

