# gen-algorithm-string-matcher
This script simulates the process of natural selection (Darwinian Theory) to find the most optimal solution—in this case, guessing the input target word.

---
## Brief History
Genetic Algorithm is an algorithm that replicate how the theory of natural selection (Darwinian theory) works. The Genetic Algorithm as we know it today was formally invented by John Holland in 1975 at the University of Michigan. He published the groundbreaking book "Adaptation in Natural and Artificial Systems". Holland was the first to mathematically formalize the concept of "crossover" (recombination) and represent artificial genetics as binary strings.

In 1989, David E. Goldberg, a student of Holland, published "Genetic Algorithms in Search, Optimization, and Machine Learning". This book made the math accessible and sparked a massive wave of practical applications across industries, just as this program aims to do.

---
## Program Workflow
- ### Data Representation and Fitness
  - Chromosomes (Individuals)
    Each individual in the population is an array of numbers, where each number corresponds to a letter (1 for A, 2 for B, ... 26 for Z).
    
  - Fitness Calculation
    This function determines how "good" a chromosome is. It calculates the absolute difference between each letter in the chromosome and the target word. The total difference is then subtracted from the maximum possible difference, meaning a higher score represents a better match.

- ### Evolution Cycle
  - Selection
    It selects two "parents" from the current population. It uses a "roulette wheel" method, meaning chromosomes with higher fitness scores have a proportionally higher chance of being picked.
    
  - Crossover
    The two parents are combined to create two "children" using a single-point crossover. It picks a random split point and swaps the parts between the parents, mixing their genetic material.

  - Mutation
    The children have a chance (determined by the mutation rate) to randomly change some of their letters. This introduces new genetic material and prevents the algorithm from getting stuck.

  - Survivor Selection (Elitism)
    The algorithm uses a  $$\mu + \lambda$$ strategy where  $$\mu$$ represents the parents and  $$\lambda$$ represents the childrens. It combines the original population ($$\mu$$) with all the new children ($$\lambda$$), sorts them by their fitness, and keeps only the top individuals for the next generation.

- ### The Experiment Grid Search
  Instead of just running the algorithm once, the main script performs a Grid Search to find the optimal hyperparameters where:
  - It tests multiple combinations of Population Sizes (50, 100... up to 1000) and Mutation Rates (0.1, 0.2, 0.3).
  - For each combination, it runs the genetic algorithm until the word is found.
  - After all scenarios are tested, it finds the scenario that completed in the fewest number of generations and prints out a step-by-step summary of how the word evolved in that best scenario.

---
## Running The Program
Just run autorun.bat where the batch script will automatically execute the genetic_algorithm.py inside the command prompt, allowing you to test it directly..
