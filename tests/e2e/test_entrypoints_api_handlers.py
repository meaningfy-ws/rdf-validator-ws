#!/usr/bin/python3

# test_entrypoints_api_handlers.py
# Date:  01/10/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com

"""
Test connexion/flask api views.
"""
from io import BytesIO
from unittest.mock import patch

import pytest
from werkzeug.datastructures import FileStorage


@pytest.mark.parametrize("filename",
                         ['test.rdf', 'test.trix', 'test.nq', 'test.nt', 'test.ttl', 'test.n3', 'test.jsonld'])
@patch('validator.entrypoints.api.handlers.generate_validation_report')
@patch('validator.entrypoints.api.handlers.run_file_validator')
def test_validate_file_success(mock_run_file_validator, mock_generate_validation_report,
                               filename, api_client, tmpdir):
    report = tmpdir.join('report.ttl')
    report.write('validation success')

    data = {
        'data_file': FileStorage(BytesIO(b'data file content'), filename),
        'schema_file': FileStorage(BytesIO(b''), 'schema_' + filename)
    }
    mock_run_file_validator.return_value = None, filename
    mock_generate_validation_report.return_value = str(report)

    response = api_client.post('/validate-file', data=data, content_type='multipart/form-data')

    assert response.status_code == 200
    assert 'text/ttl' in response.content_type
    assert 'validation success' in response.data.decode()


def test_validate_file_type_exception_one(api_client):
    unacceptable_filename = 'schema_file.pdf'
    data = {
        'data_file': FileStorage(BytesIO(b''), 'data_file.rdf'),
        'schema_file': FileStorage(BytesIO(b''), unacceptable_filename)
    }
    response = api_client.post('/validate-file', data=data, content_type='multipart/form-data')

    assert response.status_code == 415
    assert unacceptable_filename in response.json.get('detail')


def test_validate_file_type_exception_two(api_client):
    unacceptable_filename_1 = 'data_file.docx'
    unacceptable_filename_2 = 'schema_file.pdf'

    data = {
        'data_file': FileStorage(BytesIO(b''), unacceptable_filename_1),
        'schema_file': FileStorage(BytesIO(b''), unacceptable_filename_2)
    }

    response = api_client.post('/validate-file', data=data, content_type='multipart/form-data')

    assert response.status_code == 415
    assert unacceptable_filename_1 in response.json.get('detail')
    assert unacceptable_filename_2 in response.json.get('detail')


@pytest.mark.parametrize("filename",
                         ['shapes.rdf', 'shapes.trix', 'shapes.nq', 'shapes.nt',
                          'shapes.ttl', 'shapes.n3', 'shapes.jsonld'])
@patch('validator.entrypoints.api.handlers.generate_validation_report')
@patch('validator.entrypoints.api.handlers.prepare_eds4jinja_context')
@patch('validator.entrypoints.api.handlers.run_sparql_endpoint_validator')
def test_validate_sparql_endpoint_success(mock_run_sparql_endpoint_validator, mock_prepare_eds4jinja_context,
                                          mock_generate_validation_report, filename, api_client, tmpdir):
    report = tmpdir.join('report.html')
    report.write('validation success')
    mock_run_sparql_endpoint_validator.return_value = None, None
    mock_generate_validation_report.return_value = str(report)

    data = {
        'schema_file': FileStorage(BytesIO(b'shape file content'), filename),
        'graphs': ['shape1', 'shape2'],
        'sparql_endpoint_url': 'http://sparql.endpoint'
    }
    response = api_client.post('/validate-sparql-endpoint', data=data, content_type='multipart/form-data')

    assert mock_prepare_eds4jinja_context.called
    assert response.status_code == 200
    assert 'validation success' in response.data.decode()


def test_validate_sparql_endpoint_schema_file_type_exception(api_client):
    unacceptable_filename = 'schema_file.pdf'
    data = {
        'dataset_uri': 'http://hello',
        'schema_file': FileStorage(BytesIO(b'data file content'), unacceptable_filename),
        'graphs': ['shape1', 'shape2'],
        'sparql_endpoint_url': 'http://sparql.endpoint'
    }
    response = api_client.post('/validate-sparql-endpoint', data=data, content_type='multipart/form-data')

    assert response.status_code == 415
    assert unacceptable_filename in response.data.decode()
