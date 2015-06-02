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
            PLANETS[key] = planet

        star = dict(name=row[0], mass=row[5], radius=row[6], parsecs=row[7])
        if star['name'] not in STARS:
            STARS[star['name']] = star

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

init()
