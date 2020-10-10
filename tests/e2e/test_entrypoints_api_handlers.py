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
@patch('validator.entrypoints.api.handlers.build_report_from_file')
def test_validate_file_success_different_file_types(mock_build_report_from_file,
                                                    filename, api_client, tmpdir):
    report = tmpdir.join('report.ttl')
    report.write('validation success')

    data = {
        'data_file': FileStorage(BytesIO(b'data file content'), filename),
        'schema_file0': FileStorage(BytesIO(b''), 'schema_' + filename)
    }

    mock_build_report_from_file.return_value = str(report), 'report.ttl'

    response = api_client.post('/validate-file', data=data, content_type='multipart/form-data')

    assert response.status_code == 200
    assert 'text/turtle' in response.content_type
    assert 'validation success' in response.data.decode()


@patch('validator.entrypoints.api.handlers.build_report_from_file')
def test_validate_file_success_multiple_shacl_files_success(mock_build_report_from_file,
                                                            api_client, tmpdir):
    report = tmpdir.join('report.ttl')
    report.write('validation success')

    data = {
        'data_file': FileStorage(BytesIO(b'data file content'), 'data.ttl'),
        'schema_file0': FileStorage(BytesIO(b''), 'schema_' + 'shacl0.ttl'),
        'schema_file1': FileStorage(BytesIO(b''), 'schema_' + 'shacl1.ttl'),
        'schema_file2': FileStorage(BytesIO(b''), 'schema_' + 'shacl2.ttl'),
        'schema_file3': FileStorage(BytesIO(b''), 'schema_' + 'shacl3.ttl'),
        'schema_file4': FileStorage(BytesIO(b''), 'schema_' + 'shacl4.ttl'),
    }

    mock_build_report_from_file.return_value = str(report), 'report.ttl'

    response = api_client.post('/validate-file', data=data, content_type='multipart/form-data')

    assert response.status_code == 200
    assert 'text/turtle' in response.content_type
    assert 'validation success' in response.data.decode()


def test_validate_file_type_exception_one(api_client):
    unacceptable_filename = 'schema_file.pdf'
    data = {
        'data_file': FileStorage(BytesIO(b''), 'data_file.rdf'),
        'schema_file0': FileStorage(BytesIO(b''), unacceptable_filename)
    }
    response = api_client.post('/validate-file', data=data, content_type='multipart/form-data')

    assert response.status_code == 415
    assert unacceptable_filename in response.json.get('detail')


def test_validate_file_type_exception_two(api_client):
    unacceptable_filename_1 = 'data_file.docx'
    unacceptable_filename_2 = 'schema_file.pdf'

    data = {
        'data_file': FileStorage(BytesIO(b''), unacceptable_filename_1),
        'schema_file0': FileStorage(BytesIO(b''), unacceptable_filename_2)
    }

    response = api_client.post('/validate-file', data=data, content_type='multipart/form-data')

    assert response.status_code == 415
    assert unacceptable_filename_1 in response.json.get('detail')
    assert unacceptable_filename_2 in response.json.get('detail')


@pytest.mark.parametrize("report_extension, content_type",
                         [('ttl', 'text/turtle'), ('html', 'text/html'), ('zip', 'application/zip')])
@patch('validator.entrypoints.api.handlers.build_report_from_file')
def test_validate_file_success_different_report_extensions(mock_build_report_from_file, report_extension, content_type,
                                                           api_client, tmpdir):
    report = tmpdir.join(f'report.{report_extension}')
    report.write('validation success')

    data = {
        'data_file': FileStorage(BytesIO(b'data file content'), 'data.ttl'),
        'schema_file0': FileStorage(BytesIO(b'shacl file content'), 'shacl.ttl')
    }

    mock_build_report_from_file.return_value = str(report), f'report.{report_extension}'

    response = api_client.post(f'/validate-file?report_extension{report_extension}', data=data,
                               content_type='multipart/form-data')

    assert response.status_code == 200
    assert content_type in response.content_type
    assert 'validation success' in response.data.decode()


def test_validate_file_fail_report_extension(api_client):
    data = {
        'data_file': FileStorage(BytesIO(b'data file content'), 'data.ttl'),
        'schema_file0': FileStorage(BytesIO(b'shacl file content'), 'shacl.ttl')
    }

    invalid_extension = 'pdf'

    response = api_client.post(f'/validate-file?report_extension={invalid_extension}', data=data,
                               content_type='multipart/form-data')
    assert response.status_code == 422
    assert 'Wrong report_extension format. Accepted formats: ttl, html, zip' in response.json.get('detail')


@pytest.mark.parametrize("filename",
                         ['shapes.rdf', 'shapes.trix', 'shapes.nq', 'shapes.nt',
                          'shapes.ttl', 'shapes.n3', 'shapes.jsonld'])
@patch('validator.entrypoints.api.handlers.build_report_from_sparql_endpoint')
def test_validate_sparql_endpoint_success(mock_build_report_from_sparql_endpoint, filename, api_client, tmpdir):
    report = tmpdir.join('report.ttl')
    report.write('validation success')

    data = {
        'schema_file0': FileStorage(BytesIO(b'shape file content'), filename),
        'graphs': ['shape1', 'shape2'],
        'sparql_endpoint_url': 'http://sparql.endpoint'
    }

    mock_build_report_from_sparql_endpoint.return_value = str(report), 'report.ttl'

    response = api_client.post('/validate-sparql-endpoint', data=data, content_type='multipart/form-data')

    assert response.status_code == 200
    assert 'text/turtle' in response.content_type
    assert 'validation success' in response.data.decode()


@patch('validator.entrypoints.api.handlers.build_report_from_sparql_endpoint')
def test_validate_sparql_endpoint_multiple_shacl_files_success(mock_build_report_from_sparql_endpoint,
                                                               api_client, tmpdir):
    report = tmpdir.join('report.ttl')
    report.write('validation success')

    data = {
        'schema_file0': FileStorage(BytesIO(b''), 'schema_' + 'shacl0.ttl'),
        'schema_file1': FileStorage(BytesIO(b''), 'schema_' + 'shacl1.ttl'),
        'schema_file2': FileStorage(BytesIO(b''), 'schema_' + 'shacl2.ttl'),
        'schema_file3': FileStorage(BytesIO(b''), 'schema_' + 'shacl3.ttl'),
        'schema_file4': FileStorage(BytesIO(b''), 'schema_' + 'shacl4.ttl'),
        'graphs': ['shape1', 'shape2'],
        'sparql_endpoint_url': 'http://sparql.endpoint'
    }

    mock_build_report_from_sparql_endpoint.return_value = str(report), 'report.ttl'

    response = api_client.post('/validate-sparql-endpoint', data=data, content_type='multipart/form-data')

    assert response.status_code == 200
    assert 'text/turtle' in response.content_type
    assert 'validation success' in response.data.decode()


def test_validate_sparql_endpoint_type_exception_one(api_client):
    unacceptable_filename = 'schema_file.pdf'
    data = {
        'schema_file0': FileStorage(BytesIO(b''), unacceptable_filename),
        'graphs': ['shape1', 'shape2'],
        'sparql_endpoint_url': 'http://sparql.endpoint'
    }
    response = api_client.post('/validate-sparql-endpoint', data=data, content_type='multipart/form-data')

    assert response.status_code == 415
    assert unacceptable_filename in response.json.get('detail')


def test_validate_sparql_endpoint_fail_report_extension(api_client):
    data = {
        'schema_file0': FileStorage(BytesIO(b'shacl file content'), 'shacl.ttl'),
        'graphs': ['shape1', 'shape2'],
        'sparql_endpoint_url': 'http://sparql.endpoint'
    }

    invalid_extension = 'pdf'

    response = api_client.post(f'/validate-sparql-endpoint?report_extension={invalid_extension}', data=data,
                               content_type='multipart/form-data')
    assert response.status_code == 422
    assert 'Wrong report_extension format. Accepted formats: ttl, html, zip' in response.json.get('detail')


@pytest.mark.parametrize("report_extension, content_type",
                         [('ttl', 'text/turtle'), ('html', 'text/html'), ('zip', 'application/zip')])
@patch('validator.entrypoints.api.handlers.build_report_from_sparql_endpoint')
def test_validate_sparql_endpoint_success_different_report_extensions(build_report_from_sparql_endpoint,
                                                                      report_extension,
                                                                      content_type,
                                                                      api_client, tmpdir):
    report = tmpdir.join(f'report.{report_extension}')
    report.write('validation success')

    data = {
        'schema_file0': FileStorage(BytesIO(b'shacl file content'), 'shacl.ttl'),
        'graphs': ['shape1', 'shape2'],
        'sparql_endpoint_url': 'http://sparql.endpoint'
    }

    build_report_from_sparql_endpoint.return_value = str(report), f'report.{report_extension}'

    response = api_client.post(f'/validate-sparql-endpoint?report_extension{report_extension}', data=data,
                               content_type='multipart/form-data')

    assert response.status_code == 200
    assert content_type in response.content_type
    assert 'validation success' in response.data.decode()


def test_validate_sparql_endpoint_schema_file_type_exception(api_client):
    unacceptable_filename = 'schema_file.pdf'
    data = {
        'schema_file0': FileStorage(BytesIO(b'data file content'), unacceptable_filename),
        'graphs': ['shape1', 'shape2'],
        'sparql_endpoint_url': 'http://sparql.endpoint'
    }
    response = api_client.post('/validate-sparql-endpoint', data=data, content_type='multipart/form-data')

    assert response.status_code == 415
    assert unacceptable_filename in response.data.decode()
