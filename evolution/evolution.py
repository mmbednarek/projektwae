import numpy as np

def differential_evolution(target_function,
                           bounds,
                           seed,
                           mut=0.8,
                           crossp=0.7,
                           k = 5,
                           population_size=20,
                           iteration_count=20):
    rng = np.random.RandomState(seed)
    dimensions = len(bounds)

    popluation = rng.rand(population_size, dimensions)

    min_b, max_b = np.asarray(bounds).T
    diff = np.fabs(min_b - max_b)
    population_den = min_b + popluation * diff

    fitness = np.asarray([target_function(ind) for ind in population_den])
    optimum_idx = np.argmin(fitness)
    optimum = population_den[optimum_idx]

    def pop_diversity():
        pop = np.asarray(popluation)
        mean_values = pop.mean(axis=0)
        return np.sqrt(np.square(pop - mean_values).sum(axis=0)).sum()/dimensions

    for _ in range(iteration_count):
        for j in range(population_size):
            idxs = [idx for idx in range(population_size) if idx != j]
            a, b, c = popluation[rng.choice(idxs, 3, replace = False)]

            mutant = np.clip(a + mut * (b - c), 0, 1)
            cross_points = rng.rand(dimensions) < crossp
            if not np.any(cross_points):
                cross_points[rng.randint(0, dimensions)] = True

            trial = np.where(cross_points, mutant, popluation[j])
            trial_denorm = min_b + trial * diff

            f = target_function(trial_denorm)
            if f < fitness[j]:
                fitness[j] = f
                popluation[j] = trial
                if f < fitness[optimum_idx]:
                    optimum_idx = j
                    optimum = trial_denorm
        yield optimum, fitness[optimum_idx], pop_diversity()

def differential_evolution_dg(target_function,
                           bounds,
                           seed,
                           mut=2.0,
                           crossp=0.7,
                           k = 3,
                           population_size=30,
                           iteration_count=20):
    rng = np.random.RandomState(seed)
    dimensions = len(bounds)

    popluation = rng.rand(population_size, dimensions)

    min_b, max_b = np.asarray(bounds).T
    diff = np.fabs(min_b - max_b)
    population_den = min_b + popluation * diff

    fitness = np.asarray([target_function(ind) for ind in population_den])
    optimum_idx = np.argmin(fitness)
    optimum = population_den[optimum_idx]

    def pop_diversity():
        pop = np.asarray(popluation)
        mean_values = pop.mean(axis=0)
        return np.sqrt(np.square(pop - mean_values).sum(axis=0)).sum()/dimensions

    for _ in range(iteration_count):
        for j in range(population_size):
            idxs = [idx for idx in range(population_size) if idx != j]
            a, b, c = popluation[rng.choice(idxs, 3, replace = False)]

            distance_to_a = np.partition(np.linalg.norm(np.asarray(popluation) - np.asarray(a), axis=1), k)
            n_population = distance_to_a[:k]
            non_n_population = distance_to_a[k:]
            y = rng.choice(n_population)
            z = rng.choice(non_n_population)

            mut_k = rng.uniform(0, mut, dimensions)
            mut1 = rng.uniform(-1, 1, dimensions) * y * mut_k
            mut2 = rng.uniform(-1, 1, dimensions) * z * mut_k

            mutant1 = np.clip(a + mut1 * (b - c), 0, 1)
            mutant2 = np.clip(a + mut2 * (b - c), 0, 1)

            cross_points = rng.rand(dimensions) < crossp
            if not np.any(cross_points):
                cross_points[rng.randint(0, dimensions)] = True

            trial1 = np.where(cross_points, mutant1, popluation[j])
            trial2 = np.where(cross_points, mutant2, popluation[j])
            trial = np.array([])

            trial_denorm1 = min_b + trial1 * diff
            trial_denorm2 = min_b + trial2 * diff
            trial_denorm = np.array([])

            f1 = target_function(trial_denorm1)
            f2 = target_function(trial_denorm2)
            f = .0

            if f1 < f2:
                f = f1
                trial = trial1
                trial_denorm = trial_denorm1
            else:
                f = f2
                trial = trial2
                trial_denorm = trial_denorm2

            if f < fitness[j]:
                fitness[j] = f
                popluation[j] = trial
                if f < fitness[optimum_idx]:
                    optimum_idx = j
                    optimum = trial_denorm
        yield optimum, fitness[optimum_idx], pop_diversity()

