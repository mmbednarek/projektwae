from __future__ import division, print_function
from projektwae.evolution import differential_evolution, differential_evolution_dg
from math import sin, cos, sqrt
import unittest
import numpy as np
import csv

def get_error(result, expected):
    return np.linalg.norm(np.asarray(expected) - np.asarray(result))

def as_handler(func):
    return lambda args: func(*args)

def get_log_path(testname, diversity_guided):
    if diversity_guided:
        return "logs/" + testname + ".dg.csv"
    return "logs/" + testname + ".csv"

dimension_names = ['x', 'y', 'z', 'r']

def make_header_column(dimension_count):
    header = ["iteration"]
    for name in dimension_names[:dimension_count]:
        header.append(name)
    header.append("value")
    header.append("error")
    header.append("value_error")
    return header

def make_column(iteration, points, value, error, value_error):
    column = [iteration]
    for point in points:
        column.append(point)
    column.append(value)
    column.append(error)
    column.append(value_error)
    return column

class IterationLog:
    def __init__(self, filename = "log.csv", dimension_count = 1):
        self.filename = filename
        self.dimension_count = dimension_count
        self.iteration = 0

    def __enter__(self):
        self.file = open(self.filename, 'w')
        self.writer = csv.writer(self.file)
        self.writer.writerow(make_header_column(self.dimension_count))
        return self

    def __exit__(self, *args):
        _ = args
        self.file.close()

    def log(self, optimum, optimum_value, error, value_error):
        self.iteration += 1
        self.writer.writerow(make_column(self.iteration, optimum, optimum_value, error, value_error))

class TestCaseBuilder:
    def __init__(self, test_handle, name):
        self.test_handle = test_handle
        self.name = name
        self.iteration_count = 100
        self.expected_minimum = None
        self.expected_minimum_set = None
        self.expected_minimum_toleration = None

    def with_bounds(self, bounds):
        self.bounds = bounds
        return self

    def with_target_func(self, target_func):
        self.target_func = target_func
        return self

    def with_iteration_count(self, count):
        self.iteration_count = count
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


    def run(self, diversity_guided = False):
        if self.bounds == None or self.target_func == None:
            self.test_handle.fail("test lacks bounds or target func")
            return self

        evolution_func = differential_evolution
        if diversity_guided:
            evolution_func = differential_evolution_dg

        with IterationLog(get_log_path(self.name, diversity_guided), len(self.bounds)) as logger:
            point, value = None, None
            for result in evolution_func(as_handler(self.target_func), self.bounds, iteration_count=self.iteration_count):
                point, value = result
                logger.log(point, value, self.get_error(point), self.expected_minimum_value - value)

        if self.expected_minimum_toleration != None:
            self.test_handle.assertLessEqual(self.get_error(point), self.expected_minimum_toleration)

        if self.expected_minimum_value != None:
            self.test_handle.assertLessEqual(self.expected_minimum_value - value, self.expected_minimum_value_toleration)

        return self


class UtilTest(unittest.TestCase):
    def test_get_error(self):
        self.assertGreater(get_error([1, 0, 1], [0, 1, 0]), 0.5)
        self.assertLess(get_error([1, 1, 1], [1, 1, 0.9]), 0.1)

    def test_as_handler(self):
        target_func = lambda x, y: (x - 1)**2 + (y + 2)**2
        handler = as_handler(target_func)
        self.assertEqual(handler([1, -2]), 0)

class OneOptimumTest(unittest.TestCase):
    def test_parabola_at_zero(self):
        TestCaseBuilder(self, "one.parabola") \
            .with_target_func(lambda x, y: x**2 + y**2) \
            .with_bounds([(-10, 10), (-10, 10)]) \
            .expect_minimum([0, 0], toleration=1e-3) \
            .expect_minimum_value(0, toleration=1e-3) \
            .run(diversity_guided=False) \
            .run(diversity_guided=True)

    def test_parabola_3dm(self):
        TestCaseBuilder(self, "one.transposed_parabola") \
            .with_target_func(lambda x, y, z: (x - 2)**2 + (y + 1)**2 + (z - 6)**2) \
            .with_bounds([(-20, 20), (-20, 20), (-20, 20)]) \
            .expect_minimum([2, -1, 6], toleration=1e-3) \
            .expect_minimum_value(0, toleration=1e-3) \
            .run(diversity_guided=False) \
            .run(diversity_guided=True)

class TwoLocalOneGlobalTest(unittest.TestCase):
    def test_one_dimension(self):
        TestCaseBuilder(self, "two_local.single_dimension") \
            .with_target_func(lambda x: x**4 - 4.3*x**3 + 3*x**2 - 3) \
            .with_bounds([(-1, 3)]) \
            .expect_minimum([8/3], toleration=1e-2) \
            .expect_minimum_value(-12.639506, toleration=1e-3) \
            .run(diversity_guided=False) \
            .run(diversity_guided=True)
    def test_two_dimensions(self):
        TestCaseBuilder(self, "two_local.moutains") \
            .with_target_func(lambda x, y: -x**5 + 2*x**4 + 4*x**3 - 2*x**2 - 2*x*y - 2*x + y**2) \
            .with_bounds([(-2, 2), (-2, 2)]) \
            .expect_minimum([-1.14498, -1.14498], toleration=1e-2) \
            .expect_minimum_value(-2.24199, toleration=1e-3) \
            .run(diversity_guided=False) \
            .run(diversity_guided=True)

class TwoGlobalTest(unittest.TestCase):
    def test_one_dimension(self):
        TestCaseBuilder(self, "two_global") \
            .with_target_func(lambda x: x**4 - 2*x**2) \
            .with_bounds([(-2, 2)]) \
            .expect_either_minumum([[-1], [1]], toleration=1e-2) \
            .expect_minimum_value(-1, toleration=1e-3) \
            .run(diversity_guided=False) \
            .run(diversity_guided=True)

class MultipleLocalTest(unittest.TestCase):
    def test_one_dimension(self):
        TestCaseBuilder(self, "multiple_local") \
            .with_target_func(lambda x, y: -5 * cos(x**2 + y**2) / (sqrt(x**2 + y**2 + 1))) \
            .with_bounds([(-8, 8), (-8, 8)]) \
            .expect_minimum([0, 0], toleration=1e-2) \
            .expect_minimum_value(-5, toleration=1e-3) \
            .run(diversity_guided=False) \
            .run(diversity_guided=True)

class MultipleGlobal(unittest.TestCase):
    def test_one_dimension(self):
        TestCaseBuilder(self, "multiple_global") \
            .with_target_func(lambda x, y: -2*sin(x**2 + y**2) / sqrt(x**2 + y**2)) \
            .with_bounds([(-8, 8), (-8, 8)]) \
            .expect_minimum_value(-1.7025, toleration=1e-3) \
            .run(diversity_guided=False) \
            .run(diversity_guided=True)

if __name__ == '__main__':
    unittest.main()
