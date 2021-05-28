#!/usr/bin/env python2
"""
COCO Benchmark
"""
from __future__ import division, print_function
import cocoex
from projektwae.evolution import differential_evolution

def main():
    suite_name = "bbob"
    output_folder = "benchmark-output"

    suite = cocoex.Suite(suite_name, "", "")
    budget_multiply = 1e4
    observer = cocoex.Observer(suite_name, "result_folder: " + output_folder)

    for problem in suite:
        if problem.number_of_objectives > 1:
            continue
        observer.observe(problem)
        differential_evolution(problem, problem.constraint)

if __name__ == '__main__':
    main()
