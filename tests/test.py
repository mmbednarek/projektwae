from __future__ import division, print_function

import random
import unittest

import sys
from math import sin, cos, sqrt
from projektwae.evolution import differential_evolution, differential_evolution_dg
from projektwae.util import get_error, as_handler, IterationLog

base_seed = 10000000


def get_seed():
    if len(sys.argv) >= 2:
        res, sys.argv[1:] = sys.argv[1], sys.argv[2:]
        try:
            res = int(res)
            return res
        except ValueError:
            pass
    return random.randint(0, 1000000000)


def get_log_path(testname, diversity_guided, attempt):
    if diversity_guided:
        return "logs/" + testname + ".dg." + str(attempt) + ".csv"
    return "logs/" + testname + "." + str(attempt) + ".csv"


class TestCaseBuilder:
    def __init__(self, test_handle, name):
        self.test_handle = test_handle
        self.name = name
        self.iteration_count = 100
        self.expected_minimum = None
        self.expected_minimum_set = None
        self.expected_minimum_toleration = None
        self.base_seed = base_seed
        self.attempts = 1

    def with_bounds(self, bounds):
        self.bounds = bounds
        return self

    def with_target_func(self, target_func):
        self.target_func = target_func
        return self

    def with_iteration_count(self, count):
        self.iteration_count = count
        return self

    def with_attempts(self, attempts):
        self.attempts = attempts
        return self

    def expect_minimum(self, minimum, toleration):
        self.expected_minimum = minimum
        self.expected_minimum_toleration = toleration
        return self

    def expect_either_minumum(self, minimums, toleration):
        self.expected_minimum_set = minimums
        self.expected_minimum_toleration = toleration
        return self

    def expect_minimum_value(self, value, toleration):
        self.expected_minimum_value = value
        self.expected_minimum_value_toleration = toleration
        return self

    def get_error(self, point):
        if self.expected_minimum != None:
            return get_error(point, self.expected_minimum)
        if self.expected_minimum_set != None:
            error = float("inf")
            for minimum in self.expected_minimum_set:
                minimum_error = get_error(point, minimum)
                if minimum_error < error:
                    error = minimum_error
            return error
        return float("inf")

    def run(self, diversity_guided=False):
        r = random.Random()
        r.seed(self.base_seed)
        seeds = [r.randint(0, 1000000000) for _ in range(0, self.attempts)]
        if self.bounds == None or self.target_func == None:
            self.test_handle.fail("test lacks bounds or target func")
            return self

        evolution_func = differential_evolution
        if diversity_guided:
            evolution_func = differential_evolution_dg

        for attempt_id, attempt_seed in enumerate(seeds):
            with IterationLog(get_log_path(self.name, diversity_guided, attempt_id), len(self.bounds)) as logger:
                point, value = None, None
                for result in evolution_func(as_handler(self.target_func), self.bounds, attempt_seed,
                                             iteration_count=self.iteration_count):
                    point, value, diversity = result
                    logger.log(point, value, self.get_error(point), abs(self.expected_minimum_value - value), diversity)

            if not diversity_guided and self.expected_minimum_toleration != None:
                self.test_handle.assertLessEqual(self.get_error(point), self.expected_minimum_toleration)

            if not diversity_guided and self.expected_minimum_value != None:
                self.test_handle.assertLessEqual(abs(self.expected_minimum_value - value),
                                                 self.expected_minimum_value_toleration)

        return self


class UtilTest(unittest.TestCase):
    def test_get_error(self):
        self.assertGreater(get_error([1, 0, 1], [0, 1, 0]), 0.5)
        self.assertLess(get_error([1, 1, 1], [1, 1, 0.9]), 0.1)

    def test_as_handler(self):
        target_func = lambda x, y: (x - 1) ** 2 + (y + 2) ** 2
        handler = as_handler(target_func)
        self.assertEqual(handler([1, -2]), 0)


class OneOptimumTest(unittest.TestCase):
    def test_parabola_at_zero(self):
        TestCaseBuilder(self, "one.parabola") \
            .with_target_func(lambda x, y: x ** 2 + y ** 2) \
            .with_bounds([(-10, 10), (-10, 10)]) \
            .with_attempts(10) \
            .expect_minimum([0, 0], toleration=1e-07) \
            .expect_minimum_value(0, toleration=1e-15) \
            .run(diversity_guided=False) \
            .run(diversity_guided=True)

    def test_parabola_3dm(self):
        TestCaseBuilder(self, "one.transposed_parabola") \
            .with_target_func(lambda x, y, z: (x - 2) ** 2 + (y + 1) ** 2 + (z - 6) ** 2) \
            .with_bounds([(-20, 20), (-20, 20), (-20, 20)]) \
            .with_attempts(10) \
            .expect_minimum([2, -1, 6], toleration=1e-4) \
            .expect_minimum_value(0, toleration=1e-8) \
            .run(diversity_guided=False) \
            .run(diversity_guided=True)


class TwoLocalOneGlobalTest(unittest.TestCase):
    def test_one_dimension(self):
        TestCaseBuilder(self, "two_local.single_dimension") \
            .with_target_func(lambda x: x ** 4 - 4.3 * x ** 3 + 3 * x ** 2 - 3) \
            .with_bounds([(-1, 3)]) \
            .with_attempts(10) \
            .with_iteration_count(50) \
            .expect_minimum([8 / 3], toleration=1e-2) \
            .expect_minimum_value(-12.639506, toleration=1e-3) \
            .run(diversity_guided=False) \
            .run(diversity_guided=True)

    def test_two_dimensions(self):
        TestCaseBuilder(self, "two_local.moutains") \
            .with_target_func(lambda x, y: -x ** 5 + 2 * x ** 4 + 4 * x ** 3 - 2 * x ** 2 - 2 * x * y - 2 * x + y ** 2) \
            .with_bounds([(-2, 2), (-2, 2)]) \
            .with_iteration_count(100) \
            .with_attempts(10) \
            .expect_minimum([-1.14498, -1.14498], toleration=1e-4) \
            .expect_minimum_value(-2.24199, toleration=1e-5) \
            .run(diversity_guided=False) \
            .run(diversity_guided=True)


class TwoGlobalTest(unittest.TestCase):
    def test(self):
        TestCaseBuilder(self, "two_global") \
            .with_target_func(lambda x: x ** 4 - 2 * x ** 2) \
            .with_bounds([(-2, 2)]) \
            .with_iteration_count(50) \
            .with_attempts(10) \
            .expect_either_minumum([[-1], [1]], toleration=1e-5) \
            .expect_minimum_value(-1, toleration=1e-11) \
            .run(diversity_guided=False) \
            .run(diversity_guided=True)


class MultipleLocalTest(unittest.TestCase):
    def test(self):
        TestCaseBuilder(self, "multiple_local") \
            .with_target_func(lambda x, y: -5 * cos(x ** 2 + y ** 2) / (sqrt(x ** 2 + y ** 2 + 1))) \
            .with_bounds([(-8, 8), (-8, 8)]) \
            .with_attempts(10) \
            .expect_minimum([0, 0], toleration=1e-5) \
            .expect_minimum_value(-5, toleration=1e-10) \
            .run(diversity_guided=False) \
            .run(diversity_guided=True)


class MultipleGlobal(unittest.TestCase):
    def test(self):
        TestCaseBuilder(self, "multiple_global") \
            .with_target_func(lambda x, y: -2 * sin(x ** 2 + y ** 2) / sqrt(x ** 2 + y ** 2)) \
            .with_bounds([(-8, 8), (-8, 8)]) \
            .with_iteration_count(20) \
            .with_attempts(10) \
            .expect_minimum_value(-1.7025, toleration=1e-1) \
            .run(diversity_guided=False) \
            .run(diversity_guided=True)

if __name__ == '__main__':
    base_seed = get_seed()
    print("seed: " + str(base_seed))

if __name__ == '__main__':
    unittest.main()
