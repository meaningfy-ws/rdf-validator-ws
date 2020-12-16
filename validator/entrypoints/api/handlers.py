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

from validator.config import RDF_VALIDATOR_LOGGER
from validator.entrypoints.api.helpers import _guess_file_type, INPUT_MIME_TYPES, REPORT_EXTENSIONS, \
    DEFAULT_REPORT_EXTENSION
from validator.service_layer.handlers import build_report_from_file, build_report_from_sparql_endpoint

logger = logging.getLogger(RDF_VALIDATOR_LOGGER)


def validate_file(data_file: FileStorage,
                  schema_file0: FileStorage, schema_file1: FileStorage = None, schema_file2: FileStorage = None,
                  schema_file3: FileStorage = None, schema_file4: FileStorage = None,
                  report_extension: str = DEFAULT_REPORT_EXTENSION) -> tuple:
    """
    API method to handle file validation.
    :param data_file: The file to be validated
    :param schema_file0 - schema_file4: The content of the SHACL shape files defining the validation constraints
    :param report_extension: type of file to be returned. Can be `html`, `ttl`, or `zip`. Defaults to `ttl`
    :return: the validation report in the requested format
    :rtype: report file (html, ttl or zip format), int
    """
    logger.debug('start validate file endpoint')

    schema_files = list()
    for schema_file in [schema_file0, schema_file1, schema_file2, schema_file3, schema_file4]:
        if schema_file:
            schema_files.append(schema_file)

    file_exceptions = list()
    for file in [data_file, *schema_files]:
        if not _guess_file_type(file.filename):
            file_exceptions.append(file.filename)
    if file_exceptions:
        exception_text = 'File type errors: ' + ', '.join(file_exceptions) + '. Acceptable types: ' + \
                         ', '.join([f'{key}({value})' for (key, value) in INPUT_MIME_TYPES.items()]) + '.'
        logger.exception(exception_text)
        raise UnsupportedMediaType(exception_text)  # 415

    if report_extension not in REPORT_EXTENSIONS:
        exception_text = 'Wrong report_extension format. Accepted formats: ' \
                         f'{", ".join([format for format in REPORT_EXTENSIONS])}'
        logger.exception(exception_text)
        raise UnprocessableEntity(exception_text)  # 422

    try:
        with tempfile.TemporaryDirectory() as temp_folder:
            local_data_file = Path(temp_folder) / str(data_file.filename)
            data_file.save(local_data_file)

            local_schema_files = list()
            for schema_file in schema_files:
                local_schema_file = Path(temp_folder) / str(schema_file.filename)
                schema_file.save(local_schema_file)
                local_schema_files.append(str(local_schema_file))

            report_path, report_filename = build_report_from_file(temp_folder,
                                                                  str(local_data_file),
                                                                  local_schema_files,
                                                                  report_extension, data_file.filename)
            logger.debug('finish validate file endpoint')
            return send_file(report_path, as_attachment=True, attachment_filename=report_filename)  # 200
    except Exception as e:
        logger.exception(str(e))
        raise InternalServerError(str(e))


def validate_sparql_endpoint(body,
                             schema_file0: FileStorage, schema_file1: FileStorage = None,
                             schema_file2: FileStorage = None, schema_file3: FileStorage = None,
                             schema_file4: FileStorage = None,
                             report_extension: str = DEFAULT_REPORT_EXTENSION) -> tuple:
    """
  
    :param body: a dictionary with the json fields:
        :sparql_endpoint_url - The endpoint to validate
        :graphs - An optional list of named graphs to restrict the scope of the validation
    :param schema_file0 - schema_file4: The content of the SHACL shape files defining the validation constraints
    :param report_extension: type of file to be returned. Can be `html`, `ttl`, or `zip`. Defaults to `ttl`
    :return: the validation ttl file
    :rtype: ttl file, int
    """
    logger.debug('start validate sparql endpoint')

    schema_files = list()
    for schema_file in [schema_file0, schema_file1, schema_file2, schema_file3, schema_file4]:
        if schema_file:
            schema_files.append(schema_file)

    sparql_endpoint_url = body.get('sparql_endpoint_url')
    graphs = body.get('graphs')
    file_exceptions = list()
    for file in schema_files:
        if not _guess_file_type(file.filename):
            file_exceptions.append(file.filename)
    if file_exceptions:
        exception_text = 'File type errors: ' + ', '.join(file_exceptions) + '. Acceptable types: ' + \
                         ', '.join([f'{key}({value})' for (key, value) in INPUT_MIME_TYPES.items()]) + '.'
        logger.exception(exception_text)
        raise UnsupportedMediaType(exception_text)  # 415

    if report_extension not in REPORT_EXTENSIONS:
        exception_text = 'Wrong report_extension format. Accepted formats: ' \
                         f'{", ".join([format for format in REPORT_EXTENSIONS])}'
        logger.exception(exception_text)
        raise UnprocessableEntity(exception_text)  # 422

    try:
        with tempfile.TemporaryDirectory() as temp_folder:
            local_schema_files = list()
            for schema_file in schema_files:
                local_schema_file = Path(temp_folder) / str(schema_file.filename)
                schema_file.save(local_schema_file)
                local_schema_files.append(str(local_schema_file))

            report_path, report_filename = build_report_from_sparql_endpoint(temp_folder,
                                                                             sparql_endpoint_url,
                                                                             graphs,
                                                                             local_schema_files,
                                                                             report_extension,
                                                                             'filename')
            logger.debug('finish validate sparql endpoint')
            return send_file(report_path, as_attachment=True, attachment_filename=report_filename)  # 200
    except Exception as e:
        logger.exception(str(e))
        raise InternalServerError(str(e))  # 500
