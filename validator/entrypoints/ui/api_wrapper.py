#!/usr/bin/python3

# api_wrapper.py
# Date:  24/09/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com

"""
Service to consume validator API.
"""
import requests
from werkzeug.datastructures import FileStorage

from validator.entrypoints.ui import config


def validate_file(data_file: FileStorage, schema_file: FileStorage) -> tuple:
    """
    Method to connect to the validator api to validate a file.
    :param data_file: The file to be validated
    :param schema_file: The content of the SHACL shape files defining the validation constraints
    :return: state of the api response
    :rtype: file, int
    """
    files = {
        'data_file': (data_file.filename, data_file.stream, data_file.mimetype),
        'schema_file': (schema_file.filename, schema_file.stream, schema_file.mimetype)
    }

    response = requests.post(config.VALIDATOR_API_ENDPOINT + '/validate-file', files=files)
    return response.content, response.status_code


def validate_sparql_endpoint(sparql_endpoint_url: str, schema_file: FileStorage, graphs: list = None):
    """
    Method to connect to the validator api to validate a SPARQL endpoint.
    :param sparql_endpoint_url: The endpoint to validate
    :param schema_file: The content of the SHACL shape files defining the validation constraints
    :param graphs: An optional list of named graphs to restrict the scope of the validation
    :return:
    """
    data = {
        'sparql_endpoint_url': sparql_endpoint_url,
    }

    if graphs:
        data['graphs'] = graphs

    files = {
        'schema_file': (schema_file.filename, schema_file.stream, schema_file.mimetype)
    }

    response = requests.post(config.VALIDATOR_API_ENDPOINT + '/validate-sparql-endpoint', data=data, files=files)
    return response.content, response.status_code
