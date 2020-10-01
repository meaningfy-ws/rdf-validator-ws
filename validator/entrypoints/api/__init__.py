#!/usr/bin/python3

# __init__.py
# Date:  21/09/2020
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com 

"""
Module for configuring and exposing the connexion api server using the Flask framework for API.
"""

import connexion

connexion_app = connexion.FlaskApp(__name__, specification_dir='openapi')
connexion_app.add_api('openapi.yaml')

app = connexion_app.app
