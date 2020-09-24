#!/usr/bin/python3

# handlers.py
# Date:  24/09/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com

"""
OpenAPI mehod handlers.
"""
from werkzeug.datastructures import FileStorage


def validate_endpoint(body, schema_files: FileStorage):
    """

    :param body:
    :param schema_files:
    :return:
    """
    dataset_uri = body.get('dataset_uri')
    endpoint_url = body.get('endpoint_url')
    graphs = body.get('graphs')

    # validate values
    # see how to work around the one file bug
    # use RDFUnit wrapper

    return "Success", 200
