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
    result = list()  # initially empty
    with open(file_name, encoding="utf-8") as file:
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
    for index1, city1 in enumerate(cities):
        for index2, city2 in enumerate(cities):
            if index1 < index2:
                result[index1][index2] = round(distance(city1, city2))
            elif index1 > index2:
                result[index1][index2] = result[index2][index1]
            else:
                result[index1][index2] = 0
    return result


def tour_length(tour, matrix):
    """
    Length of a tour.
    """
    return sum(matrix[tour[i]][tour[i-1]] for i in range(len(tour)))


def greedy(tour, matrix):
    """
    Greedy algorithm chooses best remaining city for each next link.
    """
    for index1 in range(1, len(tour)-1):
        current = index1-1  # current city
        best = index1       # best next city
        row = matrix[tour[current]]  # current row of distance matrix
        for index2 in range(index1+1, len(tour)):
            if row[tour[index2]] < row[tour[best]]:
                best = index2
        tour[index1], tour[best] = tour[best], tour[index1]  # swap
    return tour


def city_2_opt(tour, matrix):
    """
    Improve a tour by swapping pairs of cities.
    Compare distances before an after each possible swap.
    Continue until no improvement is possible.
    """
    improved = True
    while improved:
        improved = False
        for index1 in range(len(tour)-1):
            p1 = tour[index1-2]  # previous city
            c1 = tour[index1-1]  # current city
            n1 = tour[index1]    # next city
            d1 = matrix[c1]      # distances
            for index2 in range(index1+1, len(tour)):
                p2 = tour[index2-2]  # previous city
                c2 = tour[index2-1]  # current city
                n2 = tour[index2]    # next city
                d2 = matrix[c2]      # distances
                if c1 == p2:
                    # before: p1, c1, c2, n2
                    # after:  p1, c2, c1, n2
                    before = d1[p1] + d1[c2] + d2[n2]
                    after = d2[p1] + d2[c1] + d1[n2]
                elif c2 == p1:
                    # before: p2, c2, c1, n1
                    # after:  p2, c1, c2, n1
                    before = d2[p2] + d2[c1] + d1[n1]
                    after = d1[p2] + d1[c2] + d2[n1]
                else:
                    # before: p1, c1, n1 ... p2, c2, n2
                    # after:  p1, c2, n1 ... p2, c1, n2
                    before = d1[p1] + d1[n1] + d2[p2] + d2[n2]
                    after = d2[p1] + d2[n1] + d1[p2] + d1[n2]
                if after < before:
                    (tour[index1-1], tour[index2-1]) = (c2, c1)  # swap
                    improved = True
                    c1 = tour[index1-1]
                    d1 = matrix[c1]
    return tour


def link_2_opt(tour, matrix):
    """
    Improve a tour by swapping pairs of links.
    Compare distances before and after each possible swap.
    Continue until no improvement is possible.
    """
    improved = True
    while improved:
        improved = False
        for index1 in range(len(tour)-2):
            p1 = tour[index1-1]  # previous city
            c1 = tour[index1]    # current city
            d1 = matrix[c1]      # distances
            for index2 in range(index1+2, len(tour)):
                c2 = tour[index2-1]  # current city
                n2 = tour[index2]    # next city
                d2 = matrix[c2]      # distances
                # before: p1, c1 ... c2, n2
                # after:  p1, c2 ... c1, n2
                before = d1[p1] + d2[n2]
                after = d2[p1] + d1[n2]
                if after < before:
                    # reverse the section of the tour between the links
                    tour[index1:index2] = reversed(tour[index1:index2])
                    improved = True
                    c1 = tour[index1]
                    d1 = matrix[c1]
    return tour


def test():
    """
    Test cases.
    """
    cities = read_city_coordinates('lab10.txt')
    subset = cities[:15]
    matrix = distance_matrix(subset)
    for row in enumerate(matrix):
        print(row)
    assert 134 == matrix[0][1], f'{cities[0].name} to {cities[1].name}'
    assert 134 == matrix[1][0], f'{cities[1].name} to {cities[0].name}'
    assert 2755 == matrix[0][13], f'{cities[0].name} to {cities[13].name}'
    assert 2755 == matrix[13][0], f'{cities[13].name} to {cities[0].name}'
    minima = [min(d for d in row if d > 0) for row in matrix]
    maxima = [max(row) for row in matrix]
    print(f'Lower bound: {sum(minima)}')
    print(f'Upper bound: {sum(maxima)}')
    tour = list(range(len(subset)))
    random.shuffle(tour)
    print(f'random: {tour_length(tour, matrix)} miles {tour}')
    tour = greedy(tour, matrix)
    print(f'greedy: {tour_length(tour, matrix)} miles {tour}')
    tour = city_2_opt(tour, matrix)
    print(f'city_2_opt: {tour_length(tour, matrix)} miles {tour}')
    tour = link_2_opt(tour, matrix)
    print(f'link_2_opt: {tour_length(tour, matrix)} miles {tour}')


# random.seed(1)
test()
