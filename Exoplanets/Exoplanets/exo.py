"""
Module for confirmed exoplanets and the stars they orbit
"""

from collections import OrderedDict
import requests
import io
import csv

class Planet:
    count = 0

    def __init__(self, star, letter, date, mass, radius, method):
        self.star = star
        self.letter = letter
        self.date = date
        self.mass = mass
        self.radius = radius
        self.method = method
        Planet.count += 1
        self.id = 'p' + str(Planet.count)


class Star:
    count = 0

    def __init__(self, name, mass, radius, parsecs):
        self.name = name
        self.mass = mass
        self.radius = radius
        self.parsecs = parsecs
        self.planets = 1
        Star.count += 1
        self.id = 's' + str(Star.count)


STARS = OrderedDict()
PLANETS = OrderedDict()

def init():
    """Initialize the STARS and PLANETS collections with data from the NASA api."""
    data = requests.get('http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?' +
                        'table=exoplanets&select=pl_hostname,pl_letter,pl_publ_date,pl_masse,' +
                        'pl_rade,st_mass,st_rad,st_dist,pl_discmethod' +
                        '&where=pl_publ_date%20is%20not%20null&order=pl_publ_date%20desc' +
                        '&format=csv')

    strings = io.StringIO(data.text)
    csv_data = csv.reader(strings)
    next(csv_data)

    global PLANETS
    global STARS

    for row in csv_data:
        star_name = row[0]
        planet_letter = row[1]
        key = star_name + ' ' + planet_letter

        if key not in PLANETS:
            PLANETS[key] = Planet(star=star_name, letter=planet_letter, date=row[2], mass=row[3],
                                  radius=row[4], method=row[8])

        if star_name not in STARS:
            STARS[star_name] = Star(name=star_name, mass=row[5], radius=row[6], parsecs=row[7])
        else:
            STARS[star_name].planets += 1

def first_planet():
    """Get the first planet in the collection."""
    if len(PLANETS) > 0:
        return next(iter(PLANETS.values()))
    else:
        return None

def first_star():
    """Get the first star in the collection."""
    if len(STARS) > 0:
        return next(iter(STARS.values()))
    else:
        return None

def find_star(star_name):
    """Get a star by name."""
    return STARS[star_name]

def find_star_name(id):
    """Find the name of a star from the id"""
    name = ''
    for value in STARS.values():
        if value.id == id:
            name = value.name
            break
    return name

def find_planets(star_name):
    """Get all planets orbiting a particular star."""
    star_name = star_name.replace('*', '.')
    planets = []
    for planet in PLANETS.values():
        if planet.star == star_name:
            planets.append(planet)
    return planets

init()
