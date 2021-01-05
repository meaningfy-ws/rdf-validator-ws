#!/usr/bin/python3

# config.py
# Date: 09/10/2020
# Author: Laurentiu Mandru
# Email: mclaurentiu79@gmail.com

"""
Project wide configuration file.
"""
import logging
import os
from distutils.util import strtobool
from pathlib import Path


class classproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


class ValidatorConfig:
    logger_name = 'validator'
    logger = logging.getLogger(logger_name)

    @classproperty
    def RDF_VALIDATOR_LOGGER(cls):
        value = cls.logger_name
        cls.logger.debug(value)
        return value

    @classproperty
    def RDFUNIT_QUERY_DELAY_MS(cls):
        value = os.environ.get('RDFUNIT_QUERY_DELAY_MS', 1)
        cls.logger.debug(value)
        return value

    @classproperty
    def RDF_VALIDATOR_DEBUG(cls):
        value = strtobool(os.environ.get('RDF_VALIDATOR_DEBUG', 'true'))
        cls.logger.debug(value)
        return value

    @classproperty
    def RDF_VALIDATOR_REPORT_TEMPLATE_LOCATION(cls):
        if os.environ.get('RDF_VALIDATOR_TEMPLATE_LOCATION') \
                and Path(os.environ.get('RDF_VALIDATOR_TEMPLATE_LOCATION')).exists() \
                and any(Path(os.environ.get('RDF_VALIDATOR_TEMPLATE_LOCATION')).iterdir()):
            value = os.environ.get('RDF_VALIDATOR_TEMPLATE_LOCATION')
        else:
            value = Path(__file__).parents[1] / 'resources/templates/validator_report'
        cls.logger.debug(value)
        return value

    @classproperty
    def RDF_VALIDATOR_IS_CUSTOM(cls):
        value = strtobool(os.environ.get('RDF_VALIDATOR_IS_CUSTOM', 'false'))
        cls.logger.debug(value)
        return value

    @classproperty
    def RDF_VALIDATOR_ALLOWS_EXTRA_SHAPES(cls):
        value = strtobool(os.environ.get('RDF_VALIDATOR_ALLOWS_EXTRA_SHAPES', 'true').lower())
        cls.logger.debug(value)
        return value

    @classproperty
    def RDF_VALIDATOR_API_SERVICE(cls):
        location = os.environ.get('RDF_VALIDATOR_API_LOCATION', 'http://fingerprinter-api')
        port = os.environ.get('RDF_VALIDATOR_API_PORT', 4010)
        value = f'{location}:{port}'
        cls.logger.debug(value)
        return value

    @classproperty
    def RDF_VALIDATOR_UI_SERVICE(cls):
        location = os.environ.get('RDF_VALIDATOR_UI_LOCATION', 'http://fingerprinter-ui')
        port = os.environ.get('RDF_VALIDATOR_UI_PORT', 8010)
        value = f'{location}:{port}'
        cls.logger.debug(value)
        return value

    @classproperty
    def RDF_VALIDATOR_API_SECRET_KEY(cls):
        value = os.environ.get('RDF_VALIDATOR_API_SECRET_KEY', 'secret key api')
        cls.logger.debug(value)
        return value

    @classproperty
    def RDF_VALIDATOR_UI_SECRET_KEY(cls):
        value = os.environ.get('RDF_VALIDATOR_UI_SECRET_KEY', 'secret key api')
        cls.logger.debug(value)
        return value


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
