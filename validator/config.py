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
from typing import Optional


class ValidatorConfig:
    logger_name = 'validator'
    logger = logging.getLogger(logger_name)

    def __init__(self):
        self.check_if_valid_configuration()
        super().__init__()

    def check_if_valid_configuration(self):
        if not self.RDF_VALIDATOR_HAS_CUSTOM_SHAPES and not self.RDF_VALIDATOR_ALLOWS_EXTRA_SHAPES:
            self.logger.debug('The validator can\'t run in this configuration. '
                              'Set at least one of these variables to True: RDF_VALIDATOR_SHACL_SHAPES_PATH or '
                              'RDF_VALIDATOR_ALLOWS_EXTRA_SHAPES.')
            raise RuntimeError()

    @property
    def RDF_VALIDATOR_LOGGER(self) -> str:
        value = self.logger_name
        self.logger.debug(value)
        return value

    @property
    def RDFUNIT_QUERY_DELAY_MS(self) -> int:
        value = int(os.environ.get('RDFUNIT_QUERY_DELAY_MS', 1))
        self.logger.debug(value)
        return value

    @property
    def RDF_VALIDATOR_DEBUG(self) -> bool:
        value = strtobool(os.environ.get('RDF_VALIDATOR_DEBUG', 'true'))
        self.logger.debug(value)
        return value

    @property
    def RDF_VALIDATOR_REPORT_TEMPLATE_LOCATION(self) -> str:
        if os.environ.get('RDF_VALIDATOR_TEMPLATE_LOCATION') \
                and Path(os.environ.get('RDF_VALIDATOR_TEMPLATE_LOCATION')).exists() \
                and any(Path(os.environ.get('RDF_VALIDATOR_TEMPLATE_LOCATION')).iterdir()):
            value = os.environ.get('RDF_VALIDATOR_TEMPLATE_LOCATION')
        else:
            value = str(Path(__file__).parents[1] / 'resources/templates/validator_report')
        self.logger.debug(value)
        return value

    @property
    def RDF_VALIDATOR_REPORT_TITLE(self) -> Optional[str]:
        value = os.environ.get('RDF_VALIDATOR_REPORT_TITLE', 'SHACL shape validation report').strip('"')
        self.logger.debug(value)
        return value

    @property
    def RDF_VALIDATOR_UI_NAME(self) -> Optional[str]:
        value = os.environ.get('RDF_VALIDATOR_UI_NAME', 'RDF Validator').strip('"')
        self.logger.debug(value)
        return value

    @property
    def RDF_VALIDATOR_HAS_CUSTOM_SHAPES(self) -> bool:
        value = strtobool(os.environ.get('RDF_VALIDATOR_HAS_CUSTOM_SHAPES', 'false').lower())
        self.logger.debug(value)
        return value

    @property
    def RDF_VALIDATOR_SHACL_SHAPES_PATH(self) -> Optional[str]:
        value = os.environ.get('RDF_VALIDATOR_SHACL_SHAPES_PATH')
        self.logger.debug(value)
        return value

    @property
    def RDF_VALIDATOR_ALLOWS_EXTRA_SHAPES(self) -> bool:
        value = strtobool(os.environ.get('RDF_VALIDATOR_ALLOWS_EXTRA_SHAPES', 'true').lower())
        self.logger.debug(value)
        return value

    @property
    def RDF_VALIDATOR_API_SERVICE(self) -> str:
        location = os.environ.get('RDF_VALIDATOR_API_LOCATION', 'http://fingerprinter-api')
        port = os.environ.get('RDF_VALIDATOR_API_PORT', 4010)
        value = f'{location}:{port}'
        self.logger.debug(value)
        return value

    @property
    def RDF_VALIDATOR_UI_SERVICE(self) -> str:
        location = os.environ.get('RDF_VALIDATOR_UI_LOCATION', 'http://fingerprinter-ui')
        port = os.environ.get('RDF_VALIDATOR_UI_PORT', 8010)
        value = f'{location}:{port}'
        self.logger.debug(value)
        return value

    @property
    def RDF_VALIDATOR_API_SECRET_KEY(self) -> str:
        value = os.environ.get('RDF_VALIDATOR_API_SECRET_KEY', 'secret key api')
        self.logger.debug(value)
        return value

    @property
    def RDF_VALIDATOR_UI_SECRET_KEY(self) -> str:
        value = os.environ.get('RDF_VALIDATOR_UI_SECRET_KEY', 'secret key api')
        self.logger.debug(value)
        return value


config = ValidatorConfig()


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
