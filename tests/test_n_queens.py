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

import os
import sys
import unittest
from subprocess import Popen, PIPE ,STDOUT

from dimod import ExactSolver

from n_queens import *

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class TestNQueens(unittest.TestCase):
    @unittest.skipIf(os.getenv('SKIP_INT_TESTS'), "Skipping integration test.")
    def test_integration(self):
        # check that nothing crashes
        demo_file = os.path.join(project_dir, 'n_queens.py')
        p = Popen([sys.executable, demo_file],
                  stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        p.stdin.write(b'4')

        output = p.communicate()[0]
        output = str(output).upper()

        # check that solution is valid
        with self.subTest(msg="Verify if output contains 'Solution is valid.' \n"):
            self.assertIn("Solution is valid.".upper(), output)

        # check that solution image was saved
        image_name = '4-queens-solution.png'
        self.assertTrue(os.path.isfile(image_name))
        os.remove(image_name)

    def test_invalid_solutions(self):
        n = 4

        # 2 queens in a column
        solution = [{0, 10, 7}, 
                    {0, 9, 6, 17}, 
                    {16, 2, 12, 7}, 
                    {11, 13, 3, 5}]
        self.assertFalse(is_valid_solution(n, solution))

        # 0 queens in a row
        solution = [{0, 9, 6, 17}, 
                    {1, 7, 11, 17}, 
                    {16, 2, 12, 7}, 
                    {11, 13, 3, 5}]
        self.assertFalse(is_valid_solution(n, solution))

    def test_4_queens(self):
        sampler = ExactSolver()

        n = 4
        solution = n_queens(n, sampler)
        self.assertEqual(len(solution), n)
        self.assertTrue(is_valid_solution(n, solution))

if __name__ == '__main__':
    unittest.main()
