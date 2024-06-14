#!/usr/bin/env python3

import math


class Point:
    coordinates = tuple()  # tuple with X and Y coordinates.

    def __init__(self, coordinates):
        assert len(coordinates) == 2, 'a point must have exactly 2 coordinates'
        self.coordinates = tuple(coordinates)

    def distance(self, other):
        """
        Euclidean distance between points.
        """
        return sum((b - a)**2 for a, b in zip(self.coordinates, other.coordinates))


class Line:
    points = tuple()  # tuple with 2 points

    def __init__(self, points):
        assert len(points) == 2, 'a line must have exactly 2 points'
        self.points = tuple(points)

    def distance(self, point):
        """
        See Distance from a point to a line: [Line defined by two points](https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line#Line_defined_by_two_points)
        """
        x0 = point.coordinates[0]
        y0 = point.coordinates[1]
        x1 = self.points[0].coordinates[0]
        y1 = self.points[0].coordinates[1]
        x2 = self.points[1].coordinates[0]
        y2 = self.points[1].coordinates[1]
        numerator = abs((y2-y1)*x0 - (x2-x1)*y0 + x2*y1 - y2*x1)
        denominator = self.points[0].distance(self.points[1])
        return numerator / denominator


def test():
    p1 = Point((1.0, 2.0))
    p2 = Point((3.0, 4.0))
    p3 = Point((1.0, 4.0))
    p4 = Point((3.0, 2.0))

    l1 = Line((p1, p2))
    l2 = Line((p3, p4))

    print(p1.distance(p2))
    print(p3.distance(p4))

    print(l1.distance(Point((5.0, 6.0))))
    print(l2.distance(Point((5.0, 0.0))))


test()
