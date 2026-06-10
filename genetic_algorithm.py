import random
import sys

# INPUT VERIFICATION
def get_word_input():
    """
    Continuously prompts the user until a valid alphabetic word is entered.
    Returns the word in uppercase.
    """
    while True:
        target_word_input = input("\nEnter the target word (letters only): ")
        if target_word_input.isalpha():
            return target_word_input.upper()
        else:
            print("Invalid input! Please ensure you only enter letters without spaces/numbers/symbols.")

# BASIC GENETIC ALGORITHM FUNCTIONS
def create_chromosome(length):
    """
    Creates a random individual (chromosome) consisting of integers 
    from 1 to 26 representing the alphabet (A=1, B=2, ..., Z=26).
    """
    return [random.randint(1, 26) for _ in range(length)]

def calculate_fitness(chromosome, target_num):
    """
    Calculates how close a chromosome is to the target.
    It computes the absolute difference between corresponding letters.
    The formula (max_possible - difference) ensures that a higher score means a better match.
    """
    difference = sum(abs(g - t) for g, t in zip(chromosome, target_num))
    return (len(target_num) * 26) - difference

def roulette_wheel_selection(population, fitnesses, total_fitness):
    """
    Selects an individual from the population using the Roulette Wheel method.
    Individuals with higher fitness have a proportionally higher chance of being selected.
    """
    if total_fitness == 0:
        return random.choice(population)
    
    # Pick a random point on the 'wheel'
    pick = random.uniform(0, total_fitness)
    current = 0
    for individual, fitness in zip(population, fitnesses):
        current += fitness
        if current > pick:
            return individual
    return population[-1]

def crossover(parent1, parent2, target_num, crossover_probability):
    """
    Combines two parents to create two children (Single-Point Crossover).
    A random cutoff point is chosen, and the genetic material is swapped.
    """
    # If the target word has length 1 or less, crossover is not possible.
    if len(target_num) <= 1 or random.random() >= crossover_probability:
        return parent1[:], parent2[:]
        
    crossover_point = random.randint(1, len(target_num) - 1)
    return (parent1[:crossover_point] + parent2[crossover_point:],
            parent2[:crossover_point] + parent1[crossover_point:])

def mutate(chromosome, mutation_rate):
    """
    Randomly changes some genes (letters) in the chromosome based on the mutation rate.
    This helps maintain genetic diversity and prevents getting stuck in local optima.
    """
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            chromosome[i] = random.randint(1, 26)
    return chromosome

# MODIFIED GA MAIN FUNCTION
def run_ga_experiment(pop_size, mut_rate, target_num, crossover_probability, max_generations=500):
    """
    Runs the genetic algorithm for a specific set of parameters.
    Uses a (Mu + Lambda) selection strategy where parents and children compete.
    """
    # Initialize the starting population with random chromosomes
    population = [create_chromosome(len(target_num)) for _ in range(pop_size)]
    generation = 0
    history_log = []
    MAX_POSSIBLE_FITNESS = len(target_num) * 26

    while generation < max_generations:
        generation += 1
        
        # Calculate fitness for every individual in the population
        fitnesses = [calculate_fitness(ind, target_num) for ind in population]
        best_fitness = max(fitnesses)
        best_index = fitnesses.index(best_fitness)
        best_chromosome = population[best_index]

        # Convert the best numeric chromosome back to a string and log it
        best_string = "".join(chr(g + 64) for g in best_chromosome)
        
        # Create a formatted string of the numeric array (genotype)
        best_numbers = " ".join(f"{g:2}" for g in best_chromosome)
        
        history_log.append(f"Gen {generation:02d}: [{best_numbers}] --- {best_string} (Fit: {best_fitness})")

        # Termination condition: Stop if the perfect match is found
        if best_fitness == MAX_POSSIBLE_FITNESS:
            return generation, history_log

        total_fitness = sum(fitnesses)

        # Generate the next generation of children
        children = []
        while len(children) < pop_size:
            # Select two parents
            p1 = roulette_wheel_selection(population, fitnesses, total_fitness)
            p2 = roulette_wheel_selection(population, fitnesses, total_fitness)
            
            # Mate them to create children
            c1, c2 = crossover(p1, p2, target_num, crossover_probability)
            
            # Mutate the children and add them to the new batch
            children.extend([mutate(c1, mut_rate), mutate(c2, mut_rate)])

        # Ensure we don't exceed the intended population size
        children = children[:pop_size]
        
        # Elitism / Survivor Selection: Combine parents and children
        combined_population = population + children

        # Sort the combined pool based on fitness (highest to lowest)
        combined_population.sort(key=lambda ind: calculate_fitness(ind, target_num), reverse=True)
        
        # Keep only the top individuals (equal to pop_size) for the next generation
        population = combined_population[:pop_size]

    return max_generations, history_log


# EXPERIMENT SCRIPT & MAIN LOOP
if __name__ == "__main__":
    greeting = "        GENETIC ALGORITHM SIMULATOR PROGRAM (WORD MATCHING)        "
    print("=" * len(greeting))
    print(greeting)
    print("=" * len(greeting))

    # 1. MAIN LOOP: Wraps the entire application
    while True:
        # Request a new word input at the start of each cycle
        target_string = get_word_input()
        
        # Convert the target string into numerical values (A=1, ..., Z=26)
        target_num = [ord(c) - 64 for c in target_string]

        # CROSSOVER PROBABILITY
        crossover_probability = 0.9

        exp_text = f"Starting Experiment for target: '{target_string}'"
        print("\n" + "#" * len(exp_text))
        print(exp_text)
        print("#" * len(exp_text))

        # Define hyperparameters grid to test
        pop_size_scenarios = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000]
        mutation_rate_scenarios = [0.1, 0.2, 0.3]
        experiment_results = []

        # Grid Search: Loop through all combinations of population sizes and mutation rates
        for pop in pop_size_scenarios:
            for mut in mutation_rate_scenarios:
                print(f"Testing Pop Size: {pop:<4} | Mut Rate: {mut} ...", end=" ")
                generations_needed, word_log = run_ga_experiment(
                    pop_size=pop,
                    mut_rate=mut,
                    target_num=target_num,
                    crossover_probability=crossover_probability
                )
                print(f"Completed in {generations_needed} generations.")

                # Store the result of each experiment
                experiment_results.append({
                    'pop_size': pop,
                    'mut_rate': mut,
                    'generations': generations_needed,
                    'history': word_log
                })

        # Find the scenario that completed in the fewest generations
        best_result = min(experiment_results, key=lambda x: x['generations'])

        print("\nEXPERIMENT SUMMARY:")
        print(f">> Population Size : {best_result['pop_size']}")
        print(f">> Mutation Rate   : {best_result['mut_rate']}")
        print(f">> Number of Generations : {best_result['generations']}")
        print(f">> Crossover Probability : {crossover_probability}")

        # Print the evolution history for the best performing scenario
        best_out = f"EVOLUTION PROCESS FOR THE BEST SCENARIO ({target_string}):"
        print("\n" + "=" * len(best_out))
        print(best_out)
        print("=" * len(best_out))

        for record in best_result['history']:
            print(record)

        print("=" * len(best_out))

        # 2. EXIT CONDITION: ask the user if they want to repeat
        repeat_query = input("\nDo you want to test another word? (y/n): ").strip().lower()

        # If the user types anything other than 'y' or 'yes', break the loop and terminate
        if repeat_query not in ['y', 'yes']:
            print("\nThank you for using this program. See you next time!")
            break
        