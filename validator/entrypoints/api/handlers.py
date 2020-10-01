#!/usr/bin/python3

# handlers.py
# Date:  24/09/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com

"""
OpenAPI method handlers.
"""
import tempfile
from pathlib import Path

from rdflib.util import guess_format
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import UnprocessableEntity

from validator.service_layer.handlers import run_file_validator

INPUT_MIME_TYPES = {
    'rdf': 'application/rdf+xml',
    'trix': 'application/xml',
    'nq': 'application/n-quads',
    'nt': 'application/n-triples',
    'jsonld': 'application/ld+json',
    'n3': 'text/n3',
    'ttl': 'text/turtle',
}


def _guess_file_type(file: str, accepted_types: dict = None):
    if accepted_types is None:
        accepted_types = INPUT_MIME_TYPES
    return guess_format(str(file), accepted_types)


def validate_file(body: dict, data_file: FileStorage, schema_file: FileStorage):
    """
    API method to handle file validation.
    :param body: a dictionary with the fields:
        :dataset_uri - The dataset URI
    :param data_file: The file to be validated
    :param schema_file: The content of the SHACL shape files defining the validation constraints
    :return:
    """
    dataset_uri = body.get('dataset_uri')

    file_exceptions = list()
    for file in [data_file.filename, schema_file.filename]:
        if not _guess_file_type(file):
            file_exceptions.append(file)
    if file_exceptions:
        exception_text = 'File type errors: ' + ', '.join(file_exceptions) + '. Acceptable types: ' + \
                         ', '.join([f'{key}({value})' for (key, value) in INPUT_MIME_TYPES.items()]) + '.'
        raise UnprocessableEntity(exception_text)

    # with tempfile.TemporaryDirectory() as temp_folder:
    #     file = Path(temp_folder) / str(data_file.filename)
    #     data_file.save(file)
    #
    #     schema_f = Path(temp_folder) / str(schema_file.filename)
    #     schema_file.save(schema_f)
    #
    #     run_file_validator(dataset_uri=str(file),
    #                        data_file=str(file),
    #                        schemas=[str(schema_f)],
    #                        output=Path(temp_folder))
    #
    #     for pa in Path(temp_folder).iterdir():
    #         print(pa)

    # validate values
    # see how to work around the one file bug
    # use RDFUnit wrapper
    return {"uri": dataset_uri,
            "data_file": str(data_file.filename),
            "file": str(schema_file.filename)}

    return "Success", 200


def validate_sparql_endpoint(body, schema_file: FileStorage):
    """
  
    :param body: a dictionary with the json fields:
        :dataset_uri - The dataset URI
        :endpoint_url - The endpoint to validate
        :graphs - An optional list of named graphs to restrict the scope of the validation
    :param schema_file: The content of the SHACL shape files defining the validation constraints
    :return:
    """
    dataset_uri = body.get('dataset_uri')
    endpoint_url = body.get('sparql_endpoint_url')
    graphs = body.get('graphs')

    # validate values
    # see how to work around the one file bug
    # use RDFUnit wrapper
    return {"uri": dataset_uri,
            "url": endpoint_url,
            "graphs": graphs,
            "file": str(schema_file.filename)}

    return "Success", 200
