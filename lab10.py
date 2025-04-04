#!/usr/bin/env python3

import math


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


def read_coordinates(file_name):
    """
    Read city coordinates from a file.
    Returns a list of tuples
      * longitude (radians)
      * latitude (radians)
      * city (string)
    """
    coordinates = list()  # initially empty
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
            city = ' '.join(words[4:])
            coordinates.append((longitude, latitude, city))
    return coordinates


for city in read_coordinates('lab10.txt'):
    print(city)
