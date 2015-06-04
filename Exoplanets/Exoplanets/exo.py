"""
Module for confirmed exoplanets and the stars they orbit
"""

from collections import OrderedDict
import requests
import io
import csv

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
        planet = dict(star=row[0], letter=row[1], date=row[2], mass=row[3], radius=row[4],
                      method=row[8])
        key = planet['star'] + ' ' + planet['letter']
        if key not in PLANETS:
            planet['id'] = 'p' + str(len(PLANETS))
            PLANETS[key] = planet

        star = dict(name=row[0], mass=row[5], radius=row[6], parsecs=row[7], planets=1)
        if star['name'] not in STARS:
            star['id'] = 's' + str(len(STARS))
            STARS[star['name']] = star
        else:
            STARS[star['name']]['planets'] += 1

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

def find_planets(star_name):
    """Get all planets orbiting a particular star."""
    planets = []
    for planet in PLANETS.values():
        if planet['star'] == star_name:
            planets.append(planet)

    return planets

init()
