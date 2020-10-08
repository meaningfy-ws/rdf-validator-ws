#!/usr/bin/python3

# handlers.py
# Date:  24/09/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com

"""
OpenAPI method handlers.
"""
import logging
import tempfile
from pathlib import Path

from flask import send_file
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import UnsupportedMediaType, InternalServerError

from validator.entrypoints.api.helpers import _guess_file_type, INPUT_MIME_TYPES
from validator.service_layer.handlers import run_file_validator, run_sparql_endpoint_validator, \
    prepare_eds4jinja_context, generate_validation_report

logger = logging.getLogger(__name__)



def validate_file(data_file: FileStorage, schema_file: FileStorage) -> tuple:
    """
    API method to handle file validation.
    :param data_file: The file to be validated
    :param schema_file: The content of the SHACL shape files defining the validation constraints
    :return: the validation ttl file
    :rtype: ttl file, int
    """
    file_exceptions = list()
    for file in [data_file.filename, schema_file.filename]:
        if not _guess_file_type(file):
            file_exceptions.append(file)
    if file_exceptions:
        exception_text = 'File type errors: ' + ', '.join(file_exceptions) + '. Acceptable types: ' + \
                         ', '.join([f'{key}({value})' for (key, value) in INPUT_MIME_TYPES.items()]) + '.'
        raise UnsupportedMediaType(exception_text)

    try:
        with tempfile.TemporaryDirectory() as temp_folder:
            local_data_file = Path(temp_folder) / str(data_file.filename)
            data_file.save(local_data_file)

            local_schema_file = Path(temp_folder) / str(schema_file.filename)
            schema_file.save(local_schema_file)

            html_report, ttl_report = run_file_validator(data_file=str(local_data_file),
                                          schemas=[str(local_schema_file)],
                                          output=str(Path(temp_folder)) + '/')

            prepare_eds4jinja_context(temp_folder, ttl_report)
            report_path = generate_validation_report(temp_folder)

            return send_file(report_path, as_attachment=True)  # 200
    except Exception as e:
        logger.exception(e)
        raise InternalServerError(str(e))


def validate_sparql_endpoint(body, schema_file: FileStorage) -> tuple:
    """
  
    :param body: a dictionary with the json fields:
        :dataset_uri - The dataset URI
        :sparql_endpoint_url - The endpoint to validate
        :graphs - An optional list of named graphs to restrict the scope of the validation
    :param schema_file: The content of the SHACL shape files defining the validation constraints
    :return: the validation ttl file
    :rtype: ttl file, int
    """
    dataset_uri = body.get('dataset_uri')
    sparql_endpoint_url = body.get('sparql_endpoint_url')
    graphs = body.get('graphs')

    if not _guess_file_type(schema_file.filename):
        exception_text = 'File type errors: ' + schema_file.filename + '. Acceptable types: ' + \
                         ', '.join([f'{key}({value})' for (key, value) in INPUT_MIME_TYPES.items()]) + '.'
        raise UnsupportedMediaType(exception_text)

    try:
        with tempfile.TemporaryDirectory() as temp_folder:
            local_schema_file = Path(temp_folder) / str(schema_file.filename)
            schema_file.save(local_schema_file)

            locations = run_sparql_endpoint_validator(dataset_uri=dataset_uri,
                                                     sparql_endpoint_uri=sparql_endpoint_url,
                                                     graphs_uris=graphs,
                                                     schemas=[str(local_schema_file)],
                                                     output=str(Path(temp_folder)) + '/')

            prepare_eds4jinja_context(temp_folder, locations[1])
            report_path = generate_validation_report(temp_folder)

            return send_file(report_path, as_attachment=True)  # 200
    except Exception as e:
        logger.exception(e)
        raise InternalServerError(str(e))
