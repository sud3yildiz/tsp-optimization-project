Comparison of Heuristic and Metaheuristic Approaches for the Traveling Salesman Problem
# Introduction
The Traveling Salesman Problem (TSP) is a classical optimization problem that aims to determine the shortest possible tour visiting each city exactly once and returning to the starting point. TSP belongs to the NP-Hard class of problems, and exact solution methods become computationally expensive as the number of cities increases.
In this study, two different approaches for solving TSP are implemented and experimentally compared:
Greedy (Nearest Neighbor) Algorithm
Genetic Algorithm
The objective is to analyze and compare their solution quality and performance behavior across different benchmark datasets.
# Methodology
# Problem Modeling
The TSP is modeled using city coordinate data. Pairwise distances between cities are computed using the Euclidean distance formula. The total tour length is defined as the sum of distances between consecutive cities in the constructed route, including the return to the starting city.
Benchmark datasets are provided in TSPLIB format and are parsed into the program using a custom parser module.
# Greedy Algorithm
The greedy algorithm is based on the nearest neighbor heuristic. Starting from a selected city, the algorithm repeatedly chooses the closest unvisited city until all cities are visited.
Characteristics of the greedy approach:
Deterministic behavior
Fast execution time
May get trapped in local optima
Sensitive to the choice of starting city
To reduce starting-point bias, the algorithm is executed from all possible starting cities, and both the best and average results are recorded.
#Genetic Algorithm
The genetic algorithm (GA) is a population-based metaheuristic designed to explore the solution space more broadly.
The following steps are implemented:
Random initialization of population
Fitness evaluation (based on total tour distance)
Tournament selection
Crossover operator
Mutation (different mutation rates are tested)
Elitism to preserve the best individual
At each generation, the best fitness value is recorded to analyze convergence behavior over time.
# Experimental Study
# Benchmark Datasets
The following TSPLIB benchmark instances are used:
Berlin11 (modified small instance)
Berlin52
KroA100
KroA150
These datasets represent different problem sizes, allowing performance observation under varying scales.
# Evaluation Criteria
The algorithms are evaluated according to:
Total tour length
Average performance over multiple runs
Standard deviation (for the Genetic Algorithm)
Performance behavior as problem size increases
The Genetic Algorithm is executed multiple times, and the following statistics are computed:
Best result
Average result
Standard deviation
The greedy algorithm is executed from all possible starting cities, and its average performance is calculated.
# Generated Outputs and Visualizations
Two main types of graphical outputs are produced:
Route Visualization Graphs
Cities are plotted in a 2D coordinate plane, and the computed tour is displayed as connected edges.
Convergence Graphs (Genetic Algorithm)
The best fitness value per generation is plotted against the generation index.
This graph illustrates improvement behavior and convergence speed.
Additionally, the effect of different mutation rates on solution quality is analyzed.
# Findings
Experimental results indicate that:
The greedy algorithm produces fast solutions but may generate suboptimal tours due to local decision-making.
The genetic algorithm generally produces shorter tours compared to the greedy approach.
However, the genetic algorithm requires higher computational cost.
As the problem size increases, the relative solution quality of the greedy algorithm decreases.
The genetic algorithm demonstrates more stable and consistent performance across larger instances.
Mutation rate significantly influences the exploration–exploitation balance.
#Conclusion
In this study, a deterministic heuristic method (Greedy Algorithm) and a population-based metaheuristic method (Genetic Algorithm) are implemented and compared for solving the Traveling Salesman Problem.
The results show that the genetic algorithm tends to provide higher-quality solutions at the cost of increased computational effort. The greedy algorithm, while efficient and simple, is limited in solution quality due to its local decision strategy.
This project provides an experimental comparison of heuristic and metaheuristic approaches and demonstrates their behavioral differences across multiple benchmark instances.
