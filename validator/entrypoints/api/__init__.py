#!/usr/bin/python3

# __init__.py
# Date:  21/09/2020
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com 

"""
Module for configuring and exposing the connexion api server using the Flask framework for API.
"""

import connexion

from validator.config import RDF_VALIDATOR_API_SECRET_KEY

connexion_app = connexion.FlaskApp(__name__, specification_dir='openapi')
connexion_app.add_api('validator.yaml')

app = connexion_app.app
app.config['SECRET_KEY'] = RDF_VALIDATOR_API_SECRET_KEY
