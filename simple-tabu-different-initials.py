from parameters import *
import copy
import random
import numpy as np

tabus = []
permutations = []
for i in range(20):
    permutations.append(np.random.permutation(num_locations))

sum = 0
for k in range(20):
    permutation = permutations[k]
    hash_permutation = [-1 for i in range(num_locations)]
    for i in range(len(permutation)):
        hash_permutation[permutation[i]] = i

    class Tabu:

        def __init__(self):
            self.age = 0

        def decrease(self,i,j):
            self.age = self.age - 1
            if (self.age == 0):
                tabus.pop(tabus.index((i,j)))
        
        def markTabu(self, row, col):
            if (len(tabus) == tabu_list_size):
                i,j = tabus.pop(0)
                tabu_list[i][j].age = 0
            self.age = tabu_tenure
            tabus.append((row, col))

    class TabuSearch:

        def swap(self, p, i, j):
            temp = p[i]
            p[i] = p[j]
            p[j] = temp

        def evaluateCandidates(self, cost):
            candidates = []
            best_candidate = ()
            best_cost = float('inf') # by how much is the candidate cost lesser than the current cost
            for i in range(num_locations):
                for j in range(num_locations):
                    if (i + j + 1 > (num_locations - 1)):
                        break
                    # make sure move is not tabu
                    if (tabu_list[i][i + j + 1].age == 0 and tabu_list[i + j + 1][i].age == 0):
                        candidates.append((i, i+j+1))
            
            # don't select whole neighbourhood, just select half
            candidates = random.sample(candidates, len(candidates)//2)
            for c in candidates:
                p = copy.deepcopy(permutation)
                i,j = c
                self.swap(p, i, j)
                current_cost = self.findCost(p)
                if (current_cost < best_cost):
                    best_cost = current_cost
                    best_candidate = (i, j)
            return best_candidate

        def findCost(self, p):
            hash_p = [-1 for i in range(num_locations)]
            c = 0
            for i in range(len(permutation)):
                hash_p[p[i]] = i
            for i in range(num_locations):
                for j in range(num_locations):
                    if (i < j and flows[i][j] != 0):
                        loc = (hash_p[i], hash_p[j])
                        c += (distances[loc[0]][loc[1]]*flows[i][j])
            return c
        
        def decreaseAges(self):
            for i in range(num_locations):
                for j in range(num_locations):
                    if (i < j and tabu_list[i][j].age != 0):
                        tabu_list[i][j].decrease(i,j)

        def tabuSearch(self):
            times = 0
            cost = self.findCost(permutation)
            stopping_criterion = (cost == optimal)
            print('initial permutation #%s %s, cost %s ' % (k+1, permutation.tolist(), cost))
            while not stopping_criterion and times != 300:
                self.decreaseAges()
                candidate = self.evaluateCandidates(cost)
                i, j = candidate
                self.swap(permutation, i, j)
                # when you mark as tabu, make sure to mark the i > j version of the candidate
                if (i > j):
                    tabu_list[j][i].markTabu(j,i)
                else:
                    tabu_list[i][j].markTabu(i,j)
                cost = self.findCost(permutation)
                stopping_criterion = (cost == optimal)
                times += 1
            return permutation, self.findCost(permutation)
                    
    tabu_list = []
    for i in range(num_locations):
        rows = []
        for j in range(num_locations):
            rows.append(Tabu())
        tabu_list.append(rows)

    search = TabuSearch().tabuSearch()
    print('best solution found and cost: ', search[0].tolist(), search[1])
    print()