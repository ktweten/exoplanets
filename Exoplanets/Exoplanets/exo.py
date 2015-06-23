"""
Module for confirmed exoplanets and the stars they orbit
"""
from mongoengine import DoesNotExist
from Exoplanets import models
import requests
import io
import csv

def init():
    """Initialize the database with data from the NASA api."""

    data = requests.get('http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?' +
                        'table=exoplanets&select=pl_hostname,pl_letter,pl_publ_date,pl_masse,' +
                        'pl_rade,st_mass,st_rad,st_dist,pl_discmethod' +
                        '&where=pl_publ_date%20is%20not%20null&order=pl_publ_date%20desc' +
                        '&format=csv')

    strings = io.StringIO(data.text)
    csv_data = csv.reader(strings)
    next(csv_data)

    for row in csv_data:
        star_name = row[0]
        planet_letter = row[1]
        key = star_name + ' ' + planet_letter

        planet = models.Planet(star_name=star_name, letter=planet_letter, date=row[2], mass=row[3],
                                  radius=row[4], method=row[8])
        planet.save()

        stars = models.Star.objects(star_name=star_name)
        if stars.count() > 0:
            star = stars[0]
        else:
            star = models.Star(star_name=star_name, mass=row[5], radius=row[6], parsecs=row[7], planets=0)

        star.planets += 1
        star.save()

def all_planets():
    """ Get all planets, ordered by the date they were published. Returns None if none are found. """
    try:
        planets = models.Planet.objects.order_by('-date')
    except DoesNotExist:
        planets = None
    return planets

def first_planet():
    """ Get the first planet in the collection. Returns None if none are found. """
    planet = models.Planet.objects.order_by('-date').first()
    return planet

def all_stars():
    """ Get all stars. Returns None if none are found. """
    try:
        stars = models.Star.objects
    except DoesNotExist:
        stars = None
    return stars

def find_star_by_id(find_id):
    """Find the star with the given id. Returns None if no star has that id."""
    try:
        star = models.Star.objects(pk=find_id)[0]
    except DoesNotExist:
        star = None
    return star

def find_planets_around_star(star):
    """Get all planets orbiting a particular star. Returns an empty list of none are found"""
    if not star:
        return []

    try:
        planets = models.Planet.objects(star_name=star.star_name)
    except DoesNotExist:
        planets = []
    return planets
