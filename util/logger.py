import csv
import os.path

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
        dirname = os.path.dirname(self.filename)
        if dirname != '' and not os.path.exists(dirname):
            os.mkdir(dirname)
        self.file = open(self.filename, 'wb+')
        self.writer = csv.writer(self.file)
        self.writer.writerow(make_header_column(self.dimension_count))
        return self

    def __exit__(self, *args):
        _ = args
        self.file.close()

    def log(self, optimum, optimum_value, error, value_error):
        self.iteration += 1
        self.writer.writerow(make_column(self.iteration, optimum, optimum_value, error, value_error))
