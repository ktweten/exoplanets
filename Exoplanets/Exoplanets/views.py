"""
Routes and views for the flask application.
"""

from flask import render_template
from Exoplanets import app
import Exoplanets.exo
import datetime

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    planet = Exoplanets.exo.first_planet()
    return render_template('index.jade', planet=planet)

@app.route('/planets')
def planets():
    """Renders all confirmed exoplanets."""
    return render_template('planets.jade', planets=Exoplanets.exo.all_planets())

@app.route('/stars')
def stars():
    """Renders all stars with confirmed exoplanets."""
    return render_template('stars.jade', stars=Exoplanets.exo.all_stars())

@app.route('/star/<id>')
def star(id):
    """Renders the star and all planets orbiting it."""
    star = Exoplanets.exo.find_star_by_id(id)
    planets = Exoplanets.exo.find_planets_around_star(star)
    return render_template('system.jade', star=star, planets=planets)
