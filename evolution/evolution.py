import numpy as np

def differential_evolution(target_function,
                           bounds,
                           mut=0.8,
                           crossp=0.7,
                           population_size=20,
                           iteration_count=20):
    """
    Implementacja ewolucji roznicowej
    """

    dimensions = len(bounds)

    popluation = np.random.rand(population_size, dimensions)

    min_b, max_b = np.asarray(bounds).T
    diff = np.fabs(min_b - max_b)
    population_den = min_b + popluation * diff

    fitness = np.asarray([target_function(ind) for ind in population_den])
    optimum_idx = np.argmin(fitness)
    optimum = population_den[optimum_idx]

    for _ in range(iteration_count):
        for j in range(population_size):
            idxs = [idx for idx in range(population_size) if idx != j]
            a, b, c = popluation[np.random.choice(idxs, 3, replace = False)]

            mutant = np.clip(a + mut * (b - c), 0, 1)
            cross_points = np.random.rand(dimensions) < crossp
            if not np.any(cross_points):
                cross_points[np.random.randint(0, dimensions)] = True

            trial = np.where(cross_points, mutant, popluation[j])
            trial_denorm = min_b + trial * diff

            f = target_function(trial_denorm)
            if f < fitness[j]:
                fitness[j] = f
                popluation[j] = trial
                if f < fitness[optimum_idx]:
                    optimum_idx = j
                    optimum = trial_denorm
        yield optimum, fitness[optimum_idx]

def differential_evolution_dg(target_function,
                              bounds,
                              mut=0.8,
                              crossp=0.7,
                              population_size=20,
                              iteration_count=20,
                              diver_low=0.05,
                              diver_high=0.3):
    dimensions = len(bounds)

    popluation = np.random.rand(population_size, dimensions)

    bound_matrix = np.asarray(bounds)
    min_b, max_b = bound_matrix.T
    diff = np.fabs(min_b - max_b)
    population_den = min_b + popluation * diff

    fitness = np.asarray([target_function(ind) for ind in population_den])
    optimum_idx = np.argmin(fitness)
    optimum = population_den[optimum_idx]

    direction_first = 1
    direction_second = 1

    def diversity(specimen):
        pop = np.asarray(popluation)
        mean_values = pop.mean(axis=0)
        return np.square(specimen - mean_values).sum(axis=0)/dimensions

    for _ in range(iteration_count):
        for j in range(population_size):
            idxs = [idx for idx in range(population_size) if idx != j]
            choice = np.random.choice(idxs, 3, replace = False)
            a, b, c = popluation[choice]

            if np.random.uniform(0, 1) > 0.5:
                b_diversity = diversity(b)

                if b_diversity < diver_low:
                    direction_first = 1
                elif b_diversity > diver_high:
                    direction_first = -1

                mutant = np.clip(a + direction_first * mut * (b - c), 0, 1)
            else:
                c_diversity = diversity(c)

                if c_diversity < diver_low:
                    direction_second = 1
                elif c_diversity > diver_high:
                    direction_second = -1

                mutant = np.clip(a + direction_second * mut * (b - c), 0, 1)

            cross_points = np.random.rand(dimensions) < crossp
            if not np.any(cross_points):
                cross_points[np.random.randint(0, dimensions)] = True
            trial = np.where(cross_points, mutant, popluation[j])
            trial_denorm = min_b + trial * diff
            f = target_function(trial_denorm)
            if f < fitness[j]:
                fitness[j] = f
                popluation[j] = trial
                if f < fitness[optimum_idx]:
                    optimum_idx = j
                    optimum = trial_denorm
        yield optimum, fitness[optimum_idx]
