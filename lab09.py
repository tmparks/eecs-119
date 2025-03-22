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
        [Distance from a point to a line: Line defined by two points](https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line#Line_defined_by_two_points)
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

    def intersects(self, point):
        """
        Determine wether or not a semi-infinte horizonal ray
        intersects the line segment.
        [Algorithm 112: Position of point relative to polygon](https://doi.org/10.1145/368637.368653)
        """
        x0 = point.coordinates[0]
        y0 = point.coordinates[1]
        x1 = self.points[0].coordinates[0]
        y1 = self.points[0].coordinates[1]
        x2 = self.points[1].coordinates[0]
        y2 = self.points[1].coordinates[1]
        return (((y1 <= y0) == (y0 < y2))
                and (((x0-x1) - (y0-y1)*(x2-x1)/(y2-y1)) < 0))


################################################################################

class Polygon:
    _vertices = list()  # ordered list of vertices
    _edges = list()     # ordered list of edges, lazily evaluated

    def __init__(self, vertices):
        assert len(vertices) >= 3, 'a polygon must have 3 or more vertices'
        self._vertices = list(vertices)
        self._edges = list()

    def _init_edges(self):
        if len(self._edges) == 0:
            self._edges = list(LineSegment((
                self._vertices[i-1],
                self._vertices[i]))
                for i in range(len(self._vertices)))

    def __eq__(self, other):
        """
        Compare to another polygon.
        """
        return (len(self._vertices) == len(other._vertices)
                and all(a == b for a, b in zip(self._vertices, other._vertices)))

    def size(self):
        """
        Get the number of vertices.
        """
        return len(self._vertices)

    def add(self, point):
        """
        Add a vertex to the polygon.
        """
        self._vertices.append(point)
        self._edges.clear()

    def delete(self, index):
        """
        Delete a vertex from the polygon.
        If fewer than 3 vertices remain, delete all vertices.
        """
        self._vertices.pop(index)
        if len(self._vertices) < 3:
            self._vertices.clear()
        self._edges.clear()

    def contains(self, point):
        """
        [Point in polygon](https://en.wikipedia.org/wiki/Point_in_polygon)
        [Algorithm 112: Position of point relative to polygon](https://doi.org/10.1145/368637.368653)
        """
        self._init_edges()
        count = sum(int(e.intersects(point)) for e in self._edges)
        return (count % 2) == 1  # odd number of intersections

    def nearest_vertex(self, point):
        """
        Find the vertex nearest to a point.
        Return the index of the nearest vertex.
        """
        nearest = 0
        min_distance = self._vertices[nearest].distance(point)
        for i in range(1, len(self._vertices)):
            distance = self._vertices[i].distance(point)
            if distance < min_distance:
                nearest = i
                min_distance = distance
        return nearest

    def vertex_distance(self, point):
        """
        Find the distance from a point to the nearest vertex.
        """
        return min(v.distance(point) for v in self._vertices)

    def edge_distance(self, point):
        """
        Find the distance from a point to the nearest edge.
        The distance is zero for points contained within the polygon.
        """
        self._init_edges()
        distance = 0.0
        if not self.contains(point):
            distance = min(e.distance(point) for e in self._edges)
        return distance


################################################################################

class Scene:
    polygons = list()  # ordered list of polygons

    def add_polygon(self, polygon):
        """
        Add a polygon to the scene.
        """
        self.polygons.append(polygon)

    def add_point(self, point):
        """
        Add a point to the polygon with the nerest vertex.
        """
        nearest = self.find_polygon_by_vertex(point)
        self.polygons[nearest].add(point)

    def delete_polygon(self, point):
        """
        Delete the polygon nearest to a point.
        """
        nearest = self.find_polygon_by_edge(point)
        self.polygons.pop(nearest)

    def delete_point(self, point):
        """
        Delete from its polygon the vertex nearest to a point.
        Delete the polygon if it has fewer than 3 remaining vertices.
        """
        nearest_polygon = self.find_polygon_by_vertex(point)
        nearest_vertex = self.polygons[nearest_polygon].nearest_vertex(point)
        self.polygons[nearest_polygon].delete(nearest_vertex)
        if self.polygons[nearest_polygon].size() < 3:
            self.polygons.pop(nearest_polygon)

    def find_polygon_by_edge(self, point):
        """
        Find the polygon with the edge nearest to a point.
        Return the index of the nearest polygon.
        """
        nearest = 0
        min_distance = self.polygons[nearest].edge_distance(point)
        for i in range(1, len(self.polygons)):
            distance = self.polygons[i].edge_distance(point)
            if distance < min_distance:
                nearest = i
                min_distance = distance
        return nearest

    def find_polygon_by_vertex(self, point):
        """
        Find the polygon with the vertex nearest to a point.
        Return the index of the nearest polygon.
        """
        nearest = 0
        min_distance = self.polygons[nearest].vertex_distance(point)
        for i in range(1, len(self.polygons)):
            distance = self.polygons[i].vertex_distance(point)
            if distance < min_distance:
                nearest = i
                min_distance = distance
        return nearest


################################################################################

def test():
    pt1 = Point((1.0, 2.0))
    pt2 = Point((3.0, 4.0))
    pt3 = Point((1.0, 4.0))
    pt4 = Point((3.0, 2.0))
    pt5 = Point((5.0, 6.0))
    pt6 = Point((5.0, 0.0))

    assert math.isclose(pt1.distance(pt2), math.sqrt(8.0))
    assert math.isclose(pt2.distance(pt3), 2.0)
    assert math.isclose(pt3.distance(pt4), math.sqrt(8.0))
    assert math.isclose(pt4.distance(pt5), math.sqrt(20.0))
    assert math.isclose(pt5.distance(pt6), 6.0)

    ln1 = Line((pt1, pt2))
    ln2 = Line((pt3, pt4))

    assert math.isclose(ln1.distance(pt5), 0)
    assert math.isclose(ln2.distance(pt6), 0)

    sg1 = LineSegment(ln1.points)
    sg2 = LineSegment(ln2.points)

    assert math.isclose(sg1.distance(pt1), 0.0)
    assert math.isclose(sg1.distance(pt2), 0.0)
    assert math.isclose(sg1.distance(pt3), ln1.distance(pt3))
    assert math.isclose(sg1.distance(pt4), ln1.distance(pt4))
    assert math.isclose(sg1.distance(pt5), pt2.distance(pt5))
    assert math.isclose(sg1.distance(pt6), ln1.distance(pt6))

    assert math.isclose(sg2.distance(pt1), ln2.distance(pt1))
    assert math.isclose(sg2.distance(pt2), ln2.distance(pt2))
    assert math.isclose(sg2.distance(pt3), 0.0)
    assert math.isclose(sg2.distance(pt4), 0.0)
    assert math.isclose(sg2.distance(pt5), ln2.distance(pt5))
    assert math.isclose(sg2.distance(pt6), pt4.distance(pt6))

    square = Polygon((
        Point((0.0, 0.0)),
        Point((2.0, 0.0)),
        Point((2.0, 2.0)),
        Point((0.0, 2.0))))

    assert math.isclose(square.vertex_distance(pt1), 1.0)
    assert math.isclose(square.vertex_distance(pt2), math.sqrt(5.0))
    assert math.isclose(square.vertex_distance(pt3), math.sqrt(5.0))
    assert math.isclose(square.vertex_distance(pt4), 1.0)
    assert math.isclose(square.vertex_distance(pt5), math.sqrt(25.0))
    assert math.isclose(square.vertex_distance(pt6), 3.0)

    assert math.isclose(square.edge_distance(pt1), 0.0)
    assert math.isclose(square.edge_distance(pt2), math.sqrt(5.0))
    assert math.isclose(square.edge_distance(pt3), 2.0)
    assert math.isclose(square.edge_distance(pt4), 1.0)
    assert math.isclose(square.edge_distance(pt5), math.sqrt(25.0))
    assert math.isclose(square.edge_distance(pt6), 3.0)

    assert not square.contains(pt1) # on edge
    assert not square.contains(pt2) # outside
    assert not square.contains(pt3) # outside
    assert not square.contains(pt4) # outside
    assert not square.contains(pt5) # outside
    assert not square.contains(pt6) # outside
    assert square.contains(Point((1.0, 1.0))) # in center


test()
