import numpy

def differential_evolution(target_function,
                           bounds,
                           mut=0.8,
                           crossp=0.7,
                           population_size=20,
                           iteration_count=1000):
    """
    Implementacja ewolucji roznicowej
    """

    dimensions = len(bounds)

    popluation = numpy.random.rand(population_size, dimensions)

    min_b, max_b = numpy.asarray(bounds).T
    diff = numpy.fabs(min_b - max_b)
    population_den = min_b + popluation * diff

    fitness = numpy.asarray([target_function(ind) for ind in population_den])
    optimum_idx = numpy.argmin(fitness)
    optimum = population_den[optimum_idx]

    for i in range(iteration_count):
        for j in range(population_size):
            idxs = [idx for idx in range(population_size) if idx != j]
            a, b, c = popluation[numpy.random.choice(idxs, 3, replace = False)]
            mutant = numpy.clip(a + mut * (b - c), 0, 1)
            cross_points = numpy.random.rand(dimensions) < crossp
            if not numpy.any(cross_points):
                cross_points[numpy.random.randint(0, dimensions)] = True
            trial = numpy.where(cross_points, mutant, popluation[j])
            trial_denorm = min_b + trial * diff
            f = target_function(trial_denorm)
            if f < fitness[j]:
                fitness[j] = f
                popluation[j] = trial
                if f < fitness[optimum_idx]:
                    optimum_idx = j
                    optimum = trial_denorm
        yield optimum, fitness[optimum_idx]
