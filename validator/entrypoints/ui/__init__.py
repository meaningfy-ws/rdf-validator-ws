#!/usr/bin/python3

# __init__.py
# Date:  21/09/2020
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com 

"""
"""

from flask import Flask
from flask_bootstrap import Bootstrap

from validator.config import RDF_VALIDATOR_UI_SECRET_KEY

app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = RDF_VALIDATOR_UI_SECRET_KEY

from . import views
