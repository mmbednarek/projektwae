#!/usr/bin/env python2
"""
COCO Benchmark
"""
from __future__ import division, print_function

import random

import cocoex
from projektwae.evolution import differential_evolution, differential_evolution_dg
import numpy as np
import sys


def get_log_path(testname, diversity_guided):
    if diversity_guided:
        return "logs/coco/" + testname + ".dg.csv"
    return "logs/coco/" + testname + ".csv"


def get_seed():
    if len(sys.argv) >= 3:
        try:
            res = int(sys.argv[2])
            return res
        except ValueError:
            pass
    return random.randint(0, 1000000000)


def main():
    suite_name = "bbob"
    output_folder = "benchmark-output"

    suite = cocoex.Suite(suite_name, "", "")
    observer = cocoex.Observer(suite_name, "result_folder: " + output_folder)

    if len(sys.argv) < 2:
        sys.stderr.write("invalid number of arguments")
        sys.exit(1)

    evolution_func = differential_evolution
    if sys.argv[1] == "dg":
        evolution_func = differential_evolution_dg
    elif sys.argv[1] != "classic":
        sys.stderr.write("expected either classic or dg as an argument")
        sys.exit(1)
    seed = get_seed()
    print("seed: " + str(seed))

    for problem in suite:
        if problem.number_of_objectives > 1:
            continue

        observer.observe(problem)
        bounds = np.asarray([problem.lower_bounds, problem.upper_bounds]).T
        for _ in evolution_func(problem, bounds, seed, iteration_count=100):
            pass


if __name__ == '__main__':
    main()
