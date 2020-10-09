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
from werkzeug.exceptions import UnsupportedMediaType, InternalServerError, UnprocessableEntity

from validator.entrypoints.api.helpers import _guess_file_type, INPUT_MIME_TYPES, REPORT_EXTENSIONS, \
    DEFAULT_REPORT_EXTENSION
from validator.service_layer.handlers import build_report_from_file, build_report_from_sparql_endpoint

logger = logging.getLogger(__name__)


def validate_file(data_file: FileStorage, schema_file: FileStorage,
                  report_extension: str = DEFAULT_REPORT_EXTENSION) -> tuple:
    """
    API method to handle file validation.
    :param data_file: The file to be validated
    :param schema_file: The content of the SHACL shape files defining the validation constraints
    :param report_extension: type of file to be returned. Can be `html`, `ttl`, or `zip`. Defaults to `ttl`
    :return: the validation report in the requested format
    :rtype: report file (html, ttl or zip format), int
    """
    file_exceptions = list()
    for file in [data_file.filename, schema_file.filename]:
        if not _guess_file_type(file):
            file_exceptions.append(file)
    if file_exceptions:
        exception_text = 'File type errors: ' + ', '.join(file_exceptions) + '. Acceptable types: ' + \
                         ', '.join([f'{key}({value})' for (key, value) in INPUT_MIME_TYPES.items()]) + '.'
        raise UnsupportedMediaType(exception_text)

    if report_extension not in REPORT_EXTENSIONS:
        raise UnprocessableEntity(
            'Wrong report_extension format. Accepted formats: '
            f'{", ".join([format for format in REPORT_EXTENSIONS])}')

    try:
        with tempfile.TemporaryDirectory() as temp_folder:
            local_data_file = Path(temp_folder) / str(data_file.filename)
            data_file.save(local_data_file)

            local_schema_file = Path(temp_folder) / str(schema_file.filename)
            schema_file.save(local_schema_file)

            report_path, report_filename = build_report_from_file(temp_folder,
                                                                  str(local_data_file),
                                                                  str(local_schema_file),
                                                                  report_extension, data_file.filename)

            return send_file(report_path, as_attachment=True, attachment_filename=report_filename)  # 200
    except Exception as e:
        logger.exception(e)
        raise InternalServerError(str(e))


def validate_sparql_endpoint(body, schema_file: FileStorage, report_extension: str = DEFAULT_REPORT_EXTENSION) -> tuple:
    """
  
    :param body: a dictionary with the json fields:
        :sparql_endpoint_url - The endpoint to validate
        :graphs - An optional list of named graphs to restrict the scope of the validation
    :param schema_file: The content of the SHACL shape files defining the validation constraints
    :param report_extension: type of file to be returned. Can be `html`, `ttl`, or `zip`. Defaults to `ttl`
    :return: the validation ttl file
    :rtype: ttl file, int
    """
    sparql_endpoint_url = body.get('sparql_endpoint_url')
    graphs = body.get('graphs')

    if not _guess_file_type(schema_file.filename):
        exception_text = 'File type errors: ' + schema_file.filename + '. Acceptable types: ' + \
                         ', '.join([f'{key}({value})' for (key, value) in INPUT_MIME_TYPES.items()]) + '.'
        raise UnsupportedMediaType(exception_text)

    if report_extension not in REPORT_EXTENSIONS:
        raise UnprocessableEntity(
            'Wrong report_extension format. Accepted formats: '
            f'{", ".join([format for format in REPORT_EXTENSIONS])}')

    try:
        with tempfile.TemporaryDirectory() as temp_folder:
            local_schema_file = Path(temp_folder) / str(schema_file.filename)
            schema_file.save(local_schema_file)

            report_path, report_filename = build_report_from_sparql_endpoint(temp_folder,
                                                                             sparql_endpoint_url,
                                                                             graphs,
                                                                             str(local_schema_file),
                                                                             report_extension,
                                                                             'filename')

            return send_file(report_path, as_attachment=True, attachment_filename=report_filename)  # 200
    except Exception as e:
        logger.exception(e)
        raise InternalServerError(str(e))  # 500
