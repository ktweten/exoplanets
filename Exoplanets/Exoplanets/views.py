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
    return render_template('planets.jade', planets=Exoplanets.exo.PLANETS)

@app.route('/stars')
def stars():
    """Renders all stars with confirmed exoplanets."""
    return render_template('stars.jade', stars=Exoplanets.exo.STARS)

@app.route('/star/<id>')
def star(id):
    """Renders the star and all planets orbiting it."""
    star_name = Exoplanets.exo.find_star_name(id)
    return render_template('system.jade', star=Exoplanets.exo.find_star(star_name),
                           planets=Exoplanets.exo.find_planets(star_name))

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.jade',
        title='Contact',
        year=datetime.datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.jade',
        title='About',
        year=datetime.datetime.now().year,
        message='Your application description page.'
    )
