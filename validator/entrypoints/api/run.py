#!/usr/bin/python3

# run.py
# Date:  24/09/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com

"""
Production API server through connexion definitions.
"""
from validator.config import RDF_VALIDATOR_DEBUG
from validator.entrypoints.api import app
from validator.entrypoints.flask_config import ProductionConfig, DevelopmentConfig

if RDF_VALIDATOR_DEBUG:
    app.config.from_object(DevelopmentConfig())
else:
    app.config.from_object(ProductionConfig())

if __name__ == '__main__':
    app.run()
