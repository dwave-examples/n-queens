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

from dimod import BinaryQuadraticModel

def exact_cover_bqm(problem_set, subsets):  
    """Returns a BQM for an exact cover.
 
    An exact cover is a collection of subsets of `problem_set` that contains every 
    element in `problem_set` exactly once.
    
    Args:
        problem_set : iterable
            An iterable of unique numbers.

        subsets : list(iterable(numeric))
            A list of subsets of `problem_set` used to find an exact cover.
    """
    bqm = BinaryQuadraticModel({}, {}, 0, 'BINARY')

    for element in problem_set:
        bqm.offset += 1

        for i in range(len(subsets)):    
            if element in subsets[i]:
                bqm.add_variable(i, -1)

                for j in range(i):         
                    if element in subsets[j]:
                        bqm.add_interaction(i, j, 2)

    return bqm
