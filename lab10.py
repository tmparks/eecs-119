#!/usr/bin/env python3

import collections
import math

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
    with open(file_name) as file:
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
    Assumes that the earth is a sphere.
    """
    R = 3959.0  # mean radius of the earth
    A = abs(city1.longitude - city2.longitude)
    b = math.pi/2.0 - city1.latitude
    c = math.pi/2.0 - city2.latitude
    a = math.acos(math.cos(b) * math.cos(c)
                  + math.sin(b) * math.sin(c) * math.cos(A))
    return a * R


def test():
    cities = read_city_coordinates('lab10.txt')
    assert (134 == round(distance(
        cities[0], cities[1]))), f'{cities[0].name} to {cities[1].name}'
    assert (2755 == round(distance(
        cities[0], cities[13]))), f'{cities[0].name} to {cities[13].name}'


test()
