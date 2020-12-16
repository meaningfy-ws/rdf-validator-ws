#!/usr/bin/python3

# config.py
# Date: 09/10/2020
# Author: Laurentiu Mandru
# Email: mclaurentiu79@gmail.com

"""
Project wide configuration file.
"""
import os
from pathlib import Path


RDFUNIT_QUERY_DELAY_MS = os.environ.get('RDFUNIT_QUERY_DELAY_MS', 1)
RDF_VALIDATOR_DEBUG = os.environ.get('RDF_VALIDATOR_DEBUG', True)

if os.environ.get('RDF_VALIDATOR_TEMPLATE_LOCATION') \
        and Path(os.environ.get('RDF_VALIDATOR_TEMPLATE_LOCATION')).exists() \
        and any(Path(os.environ.get('RDF_VALIDATOR_TEMPLATE_LOCATION')).iterdir()):
    RDF_VALIDATOR_REPORT_TEMPLATE_LOCATION = os.environ.get('RDF_VALIDATOR_TEMPLATE_LOCATION')
else:
    RDF_VALIDATOR_REPORT_TEMPLATE_LOCATION = Path(__file__).parents[1] / 'resources/templates/validator_report'

RDF_VALIDATOR_API_LOCATION = os.environ.get('RDF_VALIDATOR_API_LOCATION', 'http://fingerprinter-api')
RDF_VALIDATOR_API_PORT = os.environ.get('RDF_VALIDATOR_API_PORT', 4010)
RDF_VALIDATOR_API_SERVICE = str(RDF_VALIDATOR_API_LOCATION) + ":" + str(RDF_VALIDATOR_API_PORT)
RDF_VALIDATOR_API_SECRET_KEY = os.environ.get('RDF_VALIDATOR_API_SECRET_KEY', 'secret key api')

RDF_VALIDATOR_UI_LOCATION = os.environ.get('RDF_VALIDATOR_UI_LOCATION', 'http://fingerprinter-api')
RDF_VALIDATOR_UI_PORT = os.environ.get('RDF_VALIDATOR_UI_PORT', 4010)
RDF_VALIDATOR_UI_SERVICE = str(RDF_VALIDATOR_UI_LOCATION) + ":" + str(RDF_VALIDATOR_UI_PORT)
RDF_VALIDATOR_UI_SECRET_KEY = os.environ.get('RDF_VALIDATOR_UI_SECRET_KEY', 'secret key api')

RDF_VALIDATOR_LOGGER = 'validator'


class FlaskConfig:
    """
    Base Flask config
    """
    DEBUG = False
    TESTING = False


class ProductionConfig(FlaskConfig):
    """
    Production Flask config
    """


class DevelopmentConfig(FlaskConfig):
    """
    Development Flask config
    """
    DEBUG = True


class TestingConfig(FlaskConfig):
    """
    Testing Flask config
    """
    TESTING = True
    WTF_CSRF_ENABLED = False
