#!/usr/bin/env python3
# pylint: enable=useless-suppression
"""
Programing Assignment 10: The Traveling Salesman Problem
"""

import collections
import math
import random

City = collections.namedtuple('City', ['longitude', 'latitude', 'name'])


def decimal_degrees(degrees, minutes):
    """
    Convert degrees and minutes to decimal degrees.
    """
    return degrees + (minutes / 60.0)


def radians(degrees):
    """
    Convert degrees to radians.
    """
    return degrees * math.pi / 180.0


def read_city_coordinates(file_name):
    """
    Read city coordinates from a file.
    Returns a list of City tuples.
    """
    result = []  # initially empty
    with open(file_name, encoding='utf-8') as file:
        # Skip heading (2 lines)
        next(file)
        next(file)
        # Get coordinates from remaining lines
        for line in file:
            words = line.split()
            longitude = radians(decimal_degrees(
                float(words[0]), float(words[1])))
            latitude = radians(decimal_degrees(
                float(words[2]), float(words[3])))
            name = ' '.join(words[4:])
            result.append(City(longitude, latitude, name))
    return result


def distance(city1, city2):
    """
    Great circle distance between cities (miles).
    """
    # pylint: disable=invalid-name
    R = 3959.0  # mean radius of a spherical earth
    A = abs(city1.longitude - city2.longitude)
    b = math.pi/2.0 - city1.latitude
    c = math.pi/2.0 - city2.latitude
    a = math.acos(
        math.cos(b) * math.cos(c)
        + math.sin(b) * math.sin(c) * math.cos(A))
    return a * R


def distance_matrix(cities):
    """
    Symmetric NxN matrix with distances between all pairs of cities.
    """
    result = [[0 for _ in cities] for _ in cities]
    for i, city_i in enumerate(cities):
        for j, city_j in enumerate(cities):
            if i < j:
                result[i][j] = round(distance(city_i, city_j))
            elif i > j:
                result[i][j] = result[j][i]
            else:
                result[i][j] = 0
    return result


def tour_length(tour, dist):
    """
    Length of a tour.
    """
    return sum(dist[tour[i]][tour[i-1]] for i in range(len(tour)))


def nearest_neighbor(tour, dist):
    """
    Greedy algorithm chooses nearest remaining neighbor for each next link.
    """
    for i in range(1, len(tour)-1):
        p = tour[i-1]  # previous city
        c1 = tour[i]
        for j in range(i+1, len(tour)):
            c2 = tour[j]
            if dist[p][c2] < dist[p][c1]:
                (tour[i], tour[j]) = (c2, c1)  # swap
                c1 = tour[i]
    return tour


def city_2_opt(tour, dist):
    """
    Improve a tour by swapping pairs of cities.
    Compare distances before an after each possible swap.
    Continue until no improvement is possible.
    """
    improved = True
    while improved:
        improved = False
        for i in range(len(tour)-1):
            p1 = tour[i-2]  # previous city
            c1 = tour[i-1]
            n1 = tour[i]    # next city
            for j in range(i+1, len(tour)):
                p2 = tour[j-2]  # previous city
                c2 = tour[j-1]
                n2 = tour[j]    # next city
                if c1 == p2:
                    before = dist[p1][c1] + dist[c1][c2] + dist[c2][n2]
                    after = dist[p1][c2] + dist[c2][c1] + dist[c1][n2]
                elif c2 == p1:
                    before = dist[p2][c2] + dist[c2][c1] + dist[c1][n1]
                    after = dist[p2][c1] + dist[c1][c2] + dist[c2][n1]
                else:
                    before = (dist[p1][c1] + dist[c1][n1]
                              + dist[p2][c2] + dist[c2][n2])
                    after = (dist[p1][c2] + dist[c2][n1]
                             + dist[p2][c1] + dist[c1][n2])
                if after < before:
                    (tour[i-1], tour[j-1]) = (c2, c1)  # swap
                    improved = True
                    c1 = tour[i-1]
    return tour


def link_2_opt(tour, dist):
    """
    Improve a tour by swapping pairs of links.
    Compare distances before and after each possible swap.
    Continue until no improvement is possible.
    [2-opt](https://en.wikipedia.org/wiki/2-opt)
    """
    improved = True
    while improved:
        improved = False
        for i in range(len(tour)-2):
            p = tour[i-1]  # previous city
            c1 = tour[i]
            for j in range(i+2, len(tour)):
                c2 = tour[j-1]
                n = tour[j]  # next city
                before = dist[p][c1] + dist[c2][n]
                after = dist[p][c2] + dist[c1][n]
                if after < before:
                    # reverse the section of the tour between the links
                    tour[i:j] = reversed(tour[i:j])
                    improved = True
                    c1 = tour[i]
    return tour


def link_3_opt(tour, dist):
    """
    Improve a tour by rearranging sets of 3 of links.
    Compare distances before and after each possible rearrangement.
    Continue until no improvement is possible.
    [3-opt](https://en.wikipedia.org/wiki/3-opt)
    """
    improved = True
    while improved:
        improved = False
        for i in range(len(tour)-4):
            p = tour[i-1]  # previous city
            c1 = tour[i]
            for j in range(i+2, len(tour)-2):
                c2 = tour[j-1]
                c3 = tour[j]
                for k in range(j+2, len(tour)):
                    c4 = tour[k-1]  # current city
                    n = tour[k]     # next city
                    before = dist[p][c1] + dist[c2][c3] + dist[c4][n]
                    after1 = dist[p][c2] + dist[c1][c3] + dist[c4][n]
                    after2 = dist[p][c1] + dist[c2][c4] + dist[c3][n]
                    after3 = dist[p][c2] + dist[c1][c4] + dist[c3][n]
                    after4 = dist[p][c3] + dist[c4][c1] + dist[c2][n]
                    after5 = dist[p][c3] + dist[c4][c2] + dist[c1][n]
                    after6 = dist[p][c4] + dist[c3][c1] + dist[c2][n]
                    after7 = dist[p][c4] + dist[c3][c2] + dist[c1][n]
                    best = min(before, after1, after2, after3,
                               after4, after5, after6, after7)
                    if before == best:
                        continue  # no change
                    elif after1 == best:
                        tour[i:j] = reversed(tour[i:j])
                    elif after2 == best:
                        tour[j:k] = reversed(tour[j:k])
                    elif after3 == best:
                        tour[i:j] = reversed(tour[i:j])
                        tour[j:k] = reversed(tour[j:k])
                    elif after4 == best:
                        tour[i:k] = tour[j:k] + tour[i:j]
                    elif after5 == best:
                        tour[i:j] = reversed(tour[i:j])
                        tour[i:k] = tour[j:k] + tour[i:j]  # swap segments
                    elif after6 == best:
                        tour[j:k] = reversed(tour[j:k])
                        tour[i:k] = tour[j:k] + tour[i:j]  # swap segments
                    elif after7 == best:
                        tour[i:j] = reversed(tour[i:j])
                        tour[j:k] = reversed(tour[j:k])
                        tour[i:k] = tour[j:k] + tour[i:j]  # swap segments
                    else:
                        pass  # no change (should not get here!)
                    # If we get this far, the tour had been improved
                    improved = True
                    c1 = tour[i]
                    c2 = tour[j-1]
                    c3 = tour[j]
    return tour


def test():
    """
    Test cases.
    """
    cities = read_city_coordinates('lab10.txt')
    dist = distance_matrix(cities)
    assert 134 == dist[0][1], f'{cities[0].name} to {cities[1].name}'
    assert 134 == dist[1][0], f'{cities[1].name} to {cities[0].name}'
    assert 2755 == dist[0][13], f'{cities[0].name} to {cities[13].name}'
    assert 2755 == dist[13][0], f'{cities[13].name} to {cities[0].name}'
    minima = [min(d for d in row if d > 0) for row in dist]
    maxima = [max(row) for row in dist]
    print('Lower bound:', sum(minima))
    print('Upper bound:', sum(maxima))
    tour = list(range(50))
    random.shuffle(tour)
    print('random:', tour_length(tour, dist), 'miles', tour)
    tour = nearest_neighbor(tour, dist)
    print('nearest_neighbor:', tour_length(tour, dist), 'miles', tour)
    tour = city_2_opt(tour, dist)
    print('city_2_opt:', tour_length(tour, dist), 'miles', tour)
    tour = link_2_opt(tour, dist)
    print('link_2_opt:', tour_length(tour, dist), 'miles', tour)
    tour = link_3_opt(tour, dist)
    print('link_3_opt:', tour_length(tour, dist), 'miles', tour)


# random.seed(1)
test()
