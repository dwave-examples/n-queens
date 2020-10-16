# N Queens

The [n-queens problem](https://en.wikipedia.org/wiki/Eight_queens_puzzle) refers
to the problem of placing n queens on an n*n chessboard, such that no two queens
are able to attack each other.

This example demonstrates how to formulate the n-queens problem as a quadratic
unconstrained binary optimization (QUBO) problem, which we then solve with
dwave-system's LeapHybridSampler.

Here is an example output for a 6-queens problem:

```bash
[[0. 0. 0. 1. 0. 0.]
 [1. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 1. 0.]
 [0. 1. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 1.]
 [0. 0. 1. 0. 0. 0.]]
```

## Usage

To run this example:

```bash
python n_queens.py
```

## Code Overview

We formulate the n-queens problem as a [generalized exact cover
problem](https://en.wikipedia.org/wiki/Eight_queens_puzzle#Related_problems)
with four types of constraints:

1) Exactly one queen in each column.
2) Exactly one queen in each row.
3) At most one queen in each diagonal.
4) At most one queen in each anti-diagonal.

Here is a brief overview of the code:

* Represent each constraint with a unique number (id)
* Represent each position on the chessboard with a subset of constraint ids
* Form a binary quadratic model (BQM) using these subsets of constraints
* Run the problem (solve the BQM)
* Validate the solution
* Print a matrix (representing the solution on a chessboard)

## Code Specifics

Some notes to consider:

* Since there is exactly one queen on each row and column, we utilize a
  generalized version of the exact cover algorithm (specified in [1]) to
  handle the row and column constraints. This code can be found in
  exact_cover.py. Diagonal and anti-diagonal constraints are handled separately.

* Each position on the chessboard (each subset of constraint ids) becomes a
  variable in the BQM. That means that there are n**2 variables.

## References

[1] Andrew Lucas, "Ising formulations of many NP problems",
[doi:10.3389/fphy.2014.00005](https://www.frontiersin.org/articles/10.3389/fphy.2014.00005/full)

[2] Thijs Metsch, "Dancing links, algorithm X and the n-queens puzzle",
http://www.nohuddleoffense.de/2019/01/20/dancing-links-algorithm-x-and-the-n-queens-puzzle/

[3] Wikipedia contributors, "Eight queens puzzle" Wikipedia, The Free
Encyclopedia, https://en.wikipedia.org/wiki/Eight_queens_puzzle

## License

Released under the Apache License 2.0. See [LICENSE](LICENSE) file.
