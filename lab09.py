#!/usr/bin/env python3

import math


################################################################################

class Point:
    coordinates = tuple()  # tuple with X and Y coordinates.

    def __init__(self, coordinates):
        assert len(coordinates) == 2, 'a point must have exactly 2 coordinates'
        self.coordinates = tuple(coordinates)

    def __eq__(self, other):
        return self.coordinates == other.coordinates

    def distance(self, other):
        """
        Euclidean distance between points.
        """
        return math.sqrt(sum(
            (b-a)**2 for a, b in zip(self.coordinates, other.coordinates)))


################################################################################

class Line:
    points = tuple()  # tuple with 2 points
    length = 0.0  # distance between the 2 points

    def __init__(self, points):
        assert len(points) == 2, 'a line must have exactly 2 points'
        self.points = tuple(points)
        self.length = self.points[0].distance(self.points[1])

    def distance(self, point):
        """
        See [Distance from a point to a line: Line defined by two points](https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line#Line_defined_by_two_points)
        """
        x0 = point.coordinates[0]
        y0 = point.coordinates[1]
        x1 = self.points[0].coordinates[0]
        y1 = self.points[0].coordinates[1]
        x2 = self.points[1].coordinates[0]
        y2 = self.points[1].coordinates[1]
        numerator = abs((y2-y1)*x0 - (x2-x1)*y0 + x2*y1 - y2*x1)
        return numerator / self.length


################################################################################

class LineSegment(Line):
    def distance(self, point):
        x0 = point.coordinates[0]
        y0 = point.coordinates[1]
        x1 = self.points[0].coordinates[0]
        y1 = self.points[0].coordinates[1]
        x2 = self.points[1].coordinates[0]
        y2 = self.points[1].coordinates[1]
        dot_product = (x2-x1)*(x0-x1) + (y2-y1)*(y0-y1)
        if dot_product <= 0.0:
            return point.distance(self.points[0])
        elif dot_product >= self.length**2:
            return point.distance(self.points[1])
        else:
            return Line.distance(self, point)


################################################################################

class Polygon:
    vertices = list()  # ordered list of vertices
    edges = list()  # ordered list of edges

    def __init__(self, vertices):
        self.vertices = list(vertices)
        self.edges = list()

    def __eq__(self, other):
        return (len(self.vertices) == len(other.vertices)
                and all(a == b for a, b in zip(self.vertices, other.vertices)))

    def add(self, point):
        self.vertices.append(point)
        self.edges.clear()

    def delete(self, point):
        self.vertices.remove(point)
        self.edges.clear()

    def vertex_distance(self, point):
        return min(v.distance(point) for v in self.vertices)

    def edge_distance(self, point):
        if len(self.edges) == 0:
            self.edges = list(LineSegment((
                self.vertices[i],
                self.vertices[(i+1) % len(self.vertices)]))
                for i in range(len(self.vertices)))
        return min(e.distance(point) for e in self.edges)


################################################################################

class Scene:
    polygons = list()  # ordered list of polygons

    def add(self, polygon):
        self.polygons += polygon

    def delete(self, polygon):
        self.polygons.remove(polygon)


################################################################################


def test():
    p1 = Point((1.0, 2.0))
    p2 = Point((3.0, 4.0))
    p3 = Point((1.0, 4.0))
    p4 = Point((3.0, 2.0))
    p5 = Point((5.0, 6.0))
    p6 = Point((5.0, 0.0))

    assert math.isclose(p1.distance(p2), math.sqrt(8.0))
    assert math.isclose(p2.distance(p3), 2.0)
    assert math.isclose(p3.distance(p4), math.sqrt(8.0))
    assert math.isclose(p4.distance(p5), math.sqrt(20.0))
    assert math.isclose(p5.distance(p6), 6.0)

    l1 = Line((p1, p2))
    l2 = Line((p3, p4))

    assert math.isclose(l1.distance(p5), 0)
    assert math.isclose(l2.distance(p6), 0)

    s1 = LineSegment(l1.points)
    s2 = LineSegment(l2.points)

    assert math.isclose(s1.distance(p1), 0.0)
    assert math.isclose(s1.distance(p2), 0.0)
    assert math.isclose(s1.distance(p3), l1.distance(p3))
    assert math.isclose(s1.distance(p4), l1.distance(p4))
    assert math.isclose(s1.distance(p5), p2.distance(p5))
    assert math.isclose(s1.distance(p6), l1.distance(p6))

    assert math.isclose(s2.distance(p1), l2.distance(p1))
    assert math.isclose(s2.distance(p2), l2.distance(p2))
    assert math.isclose(s2.distance(p3), 0.0)
    assert math.isclose(s2.distance(p4), 0.0)
    assert math.isclose(s2.distance(p5), l2.distance(p5))
    assert math.isclose(s2.distance(p6), p4.distance(p6))

    square = Polygon((
        Point((0.0, 0.0)),
        Point((2.0, 0.0)),
        Point((2.0, 2.0)),
        Point((0.0, 2.0))))

    assert math.isclose(square.vertex_distance(p1), 1.0)
    assert math.isclose(square.vertex_distance(p2), math.sqrt(5.0))
    assert math.isclose(square.vertex_distance(p3), math.sqrt(5.0))
    assert math.isclose(square.vertex_distance(p4), 1.0)
    assert math.isclose(square.vertex_distance(p5), math.sqrt(25.0))
    assert math.isclose(square.vertex_distance(p6), 3.0)

    assert math.isclose(square.edge_distance(p1), 0.0)
    assert math.isclose(square.edge_distance(p2), math.sqrt(5.0))
    assert math.isclose(square.edge_distance(p3), 2.0)
    assert math.isclose(square.edge_distance(p4), 1.0)
    assert math.isclose(square.edge_distance(p5), math.sqrt(25.0))
    assert math.isclose(square.edge_distance(p6), 3.0)


test()
