#!/usr/bin/env python3
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
    a = math.acos(math.cos(b) * math.cos(c)
                  + math.sin(b) * math.sin(c) * math.cos(A))
    return a * R


def distance_matrix(cities):
    """
    Fill symmetric NxN matrix with distances between all pairs of cities.
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
    Return the length of a tour.
    """
    result = 0
    # pylint: disable-next=consider-using-enumerate
    for i in range(len(tour)):
        result += matrix[tour[i]][tour[i-1]]
    return result


def test():
    """
    Test cases.
    """
    cities = read_city_coordinates('lab10.txt')
    subset = cities[:]
    matrix = distance_matrix(subset)
    # for row in matrix:
    #     print(row)
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
    print(f'Random tour: {tour_length(tour, matrix)} miles')


test()
