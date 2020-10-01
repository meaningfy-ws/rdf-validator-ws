#!/usr/bin/python3

# test_entrypoints_api_handlers.py
# Date:  01/10/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com

"""
Test connexion/flask api views.
"""
from io import BytesIO

import pytest
from werkzeug.datastructures import FileStorage


@pytest.mark.parametrize("filename",
                         ['test.rdf', 'test.trix', 'test.nq', 'test.nt', 'test.ttl', 'test.n3', 'test.jsonld'])
def test_validate_file_file_type_success(filename, api_client):
    data = {
        'dataset_uri': 'http://hello',
        'data_file': FileStorage(BytesIO(b''), filename),
        'schema_file': FileStorage(BytesIO(b''), filename)

    }
    response = api_client.post('/validate-file', data=data, content_type='multipart/form-data')

    assert response.status_code == 200


def test_validate_file_type_exception_one(api_client):
    unacceptable_filename = 'schema_file.pdf'
    data = {
        'dataset_uri': 'http://hello',
        'data_file': FileStorage(BytesIO(b''), 'data_file.rdf'),
        'schema_file': FileStorage(BytesIO(b''), unacceptable_filename)

    }
    response = api_client.post('/validate-file', data=data, content_type='multipart/form-data')

    assert response.status_code == 422
    assert unacceptable_filename in response.json.get('detail')


def test_validate_file_type_exception_two(api_client):
    unacceptable_filename_1 = 'data_file.docx'
    unacceptable_filename_2 = 'schema_file.pdf'
    data = {
        'dataset_uri': 'http://hello',
        'data_file': FileStorage(BytesIO(b''), unacceptable_filename_1),
        'schema_file': FileStorage(BytesIO(b''), unacceptable_filename_2)

    }
    response = api_client.post('/validate-file', data=data, content_type='multipart/form-data')

    assert response.status_code == 422
    assert unacceptable_filename_1 in response.json.get('detail')
    assert unacceptable_filename_2 in response.json.get('detail')
