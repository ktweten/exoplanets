import mongoengine
import config

class ExoBody(mongoengine.Document):
    mass = mongoengine.FloatField()
    radius = mongoengine.FloatField()
    star_name = mongoengine.StringField(required = True)
    id = mongoengine.ObjectIdField()
    meta = {'allow_inheritance': True}


class Planet(ExoBody):
    letter = mongoengine.StringField(required = True)
    date = mongoengine.StringField()
    method = mongoengine.StringField()


class Star(ExoBody):
    distance = mongoengine.FloatField()
    planets = mongoengine.IntField()

mongoengine.connect('exo', host = 'mongodb://%(user)s:%(pwd)s@ds036638.mongolab.com:36638/exo' % config.values)
