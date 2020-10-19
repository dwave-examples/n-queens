# Copyright 2020 D-Wave Systems Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections import Counter

import numpy as np
from dimod import BinaryQuadraticModel
from dwave.system import LeapHybridSampler

from exact_cover import exact_cover_bqm

def build_subsets(n):
    """Returns a list of subsets of constraints corresponding to every 
    position on the chessboard. 

    Each constraint is represented by a unique number (id). Each subset 
    should contain:
    1) Exactly one column constraint id (0 to n-1)
    2) Exactly one row constraint id (n to 2*n-1)
    3) At most one diagonal constraint id (2*n to 4*n-4)
    4) At most one anti-diagonal constraint id (4*n-3 to 6*n-7)
    """

    subsets = []
    for x in range(n):
        for y in range(n): 
            col = x
            row = y + n 

            subset = {col, row}

            diag = x + y + (2*n - 1)
            min_diag = 2*n 
            max_diag = 4*n - 4

            if diag >= min_diag and diag <= max_diag:
                subset.add(diag)

            anti_diag = (n - 1 - x + y) + (4*n - 4)
            min_anti_diag = 4*n - 3
            max_anti_diag = 6*n - 7

            if anti_diag >= min_anti_diag and anti_diag <= max_anti_diag:
                subset.add(anti_diag)

            subsets.append(subset)
    
    return subsets

def handle_diag_constraints(bqm, subsets, diag_constraints):
    """Update bqm with diagonal (and anti-diagonal) constraints.
    Duplicates are penalized.
    """

    for constraint in diag_constraints:
        for i in range(len(subsets)):   
            if constraint in subsets[i]:
                for j in range(i):    
                    if constraint in subsets[j]:
                        bqm.add_interaction(i, j, 2)
    return bqm

def n_queens(n, sampler=None):
    """Returns a potential solution to the n-queens problem in a list of sets,
    each containing constraint ids representing a queen's location.

    Args:
        n: Number of queens to place

        sampler: A binary quadratic model sampler. Defaults to dwave-system's LeapHybridSampler.
    """

    num_row_col_constraints = 2 * n
    row_col_constraint_ids = set(range(num_row_col_constraints))

    num_diag_constraints = 4 * n - 6   # includes anti-diag constraints
    diag_constraint_ids = set(range(num_row_col_constraints, num_row_col_constraints + num_diag_constraints))

    # Build subsets of constraint ids. Each subset will become a variable in our BQM.
    subsets = build_subsets(n)
            
    # Build BQM with only row/col constraints
    bqm = exact_cover_bqm(row_col_constraint_ids, subsets)

    # Add diag/anti-diag constraints - duplicates are penalized.
    bqm = handle_diag_constraints(bqm, subsets, diag_constraint_ids)

    if sampler is None:
        sampler = LeapHybridSampler()

    response = sampler.sample(bqm)

    # Get lowest energy sample
    sample = response.first.sample

    return [subsets[i] for i in sample if sample[i]]

def is_valid_solution(n, solution):
    """Check that solution is valid by making sure all the constraints were
    followed.

    Args:
        n: Number of queens in the problem
        
        solution: A list of sets, each containing constraint ids that represent 
                  a queen's location.
    """
    count = Counter()

    for queen in solution:
        count = count + Counter(queen)

    # Check row/col constraints
    for i in range(2*n):
        if count[i] != 1:
            if i < n:
                col = i
                print("Column {} has {} queens.".format(col, count[i]))
            else:
                row = np.abs(i - (2*n - 1)) # Convert constraint id to row index
                print("Row {} has {} queens.".format(row, count[i]))

            return False

    # Check diag/anti-diag constraints
    for i in range(2*n, 4*n - 6):
        if count[i] > 1:
            if i <= 4*n - 4:
                print("Diagonal {} has {} queens.".format(i, count[i]))
            else:
                print("Anti-diagonal {} has {} queens.".format(i, count[i]))

            return False

    return True

def build_matrix_with_queens(n, queens):
    """Returns a matrix of size n*n with 1s representing queens.
    
    Args:
        n: Number of queens 

        queens: A list of sets, each containing constraint ids that represent 
                a queen's location.
    """
    matrix = np.zeros((n,n))

    for subset in queens:
        x = y = -1
        for constraint in subset:
            if constraint < n:
                x = constraint
            elif constraint >= n and constraint < 2*n:
                y = np.abs(constraint - (2*n - 1)) # Convert constraint id to row index
        
        if x != -1 and y != -1:
            matrix[y][x] = 1

    return matrix
    
if __name__ == "__main__":
    n = 10
    solution = n_queens(n)
    is_valid_solution(n, solution) 
    matrix = build_matrix_with_queens(n, solution)
    print(matrix)
