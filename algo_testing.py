import sys
import scipy.optimize as sc
import scipy as scm
import numpy as np

print(sys.maxsize)
print(sc.linear_sum_assignment(np.array([[1, 1, 3], [2, 0, 5], [3, 2, 2]])))


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


x = Person([3, 10, 8], [.6, .2, .2])
y = Person([9, 4, 2], [.5, .3, .2])

boys = []
girls = []

boys.append(x)
girls.append(y)

for i in range(len(boys)):
    for j in range(len(girls)):
        boys[i].my_scores[girls[j]] = boys[i].get_my_score(girls[j].my_attributes)

        girls[j].my_scores[boys[i]] = girls[j].get_my_score(boys[i].my_attributes)

        a = Match_Tuple(boys[i], girls[j])

print(Match_Tuple.match_tuples[frozenset({y, x})])



