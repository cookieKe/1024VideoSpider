# -*- coding: utf-8 -*-
#!/usr/bin/env python

from flask import Flask
from flask.ext.mongoengine import MongoEngine


app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {'db':'url_link'}

db = MongoEngine(app)

