#!/usr/bin/python3

# test_entrypoints_ui_views.py
# Date:  01/10/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com

"""
Test flask ui views.
"""
from collections import namedtuple
from io import BytesIO
from json import dumps
from unittest.mock import patch

from bs4 import BeautifulSoup
from werkzeug.datastructures import FileStorage

RequestResponse = namedtuple('RequestResponse', ['content', 'status_code'])


def _helper_get_request_and_parse(client, url) -> BeautifulSoup:
    response = client.get(url)
    return BeautifulSoup(response.data, 'html.parser')


def test_index(ui_client):
    ui_url = '/'
    soup = _helper_get_request_and_parse(ui_client, ui_url)

    title = soup.find('h1')
    assert 'RDF Validator' in title.get_text()

    validators = soup.find(id='validators').find_all('a')
    assert len(validators) == 2
    assert 'File Validation' in validators[0].get_text()
    assert 'SPARQL Endpoint Validation' in validators[1].get_text()


@patch('validator.entrypoints.ui.api_wrapper.requests.post')
def test_validate_file(mock_post, ui_client):
    ui_url = '/validate-file'
    mock_post.return_value = RequestResponse(b'data file content', 200)

    soup = _helper_get_request_and_parse(ui_client, ui_url)

    title = soup.find(id='title')
    assert 'Validate File' in title.get_text()

    data = {
        'dataset_uri': 'http://data.set',
        'data_file': FileStorage(BytesIO(b'data file content'), 'data.rdf'),
        'schema_file': FileStorage(BytesIO(b'schema file content'), 'schema.rdf'),
    }

    response = ui_client.post('/validate-file', data=data, follow_redirects=True,
                              content_type='multipart/form-data')

    assert response.status_code == 200
    assert b'data file content' == response.data


@patch('validator.entrypoints.ui.api_wrapper.requests.post')
def test_validate_file_type_exception(mock_post, ui_client):
    ui_url = '/validate-file'
    exception_content = 'This file type is not supported'
    exception_response = {
        'detail': exception_content
    }
    mock_post.return_value = RequestResponse(dumps(exception_response), 415)

    data = {
        'dataset_uri': 'http://data.set',
        'data_file': FileStorage(BytesIO(b'data file content'), 'data.pdf'),
        'schema_file': FileStorage(BytesIO(b'schema file content'), 'schema.pdf'),
    }

    response = ui_client.post(ui_url, data=data, follow_redirects=True,
                              content_type='multipart/form-data')
    soup = BeautifulSoup(response.data, 'html.parser')

    error_message = soup.find('div', {'class': 'alert alert-danger'})
    assert error_message.get_text() in exception_content


@patch('validator.entrypoints.ui.api_wrapper.requests.post')
def test_validate_sparql_endpoint(mock_post, ui_client):
    ui_url = '/validate-sparql-endpoint'
    mock_post.return_value = RequestResponse(b'schema file content', 200)

    soup = _helper_get_request_and_parse(ui_client, ui_url)

    title = soup.find(id='title')
    assert 'Validate SPARQL Endpoint' in title.get_text()

    data = {
        'dataset_uri': 'http://data.set',
        'endpoint_url': 'http://endpoint.url',
        'schema_file': FileStorage(BytesIO(b'schema file content'), 'schema.rdf'),
        'graphs': 'graph1 graph2'
    }

    response = ui_client.post(ui_url, data=data, follow_redirects=True,
                              content_type='multipart/form-data')

    assert response.status_code == 200
    assert b'schema file content' == response.data


@patch('validator.entrypoints.ui.api_wrapper.requests.post')
def test_validate_sparql_endpoint_type_exception(mock_post, ui_client):
    ui_url = '/validate-sparql-endpoint'
    exception_content = 'This file type is not supported'
    exception_response = {
        'detail': exception_content
    }
    mock_post.return_value = RequestResponse(dumps(exception_response), 415)

    data = {
        'dataset_uri': 'http://data.set',
        'endpoint_url': 'http://endpoint.url',
        'schema_file': FileStorage(BytesIO(b'schema file content'), 'schema.rdf'),
        'graphs': 'graph1 graph2'
    }

    response = ui_client.post(ui_url, data=data, follow_redirects=True,
                              content_type='multipart/form-data')
    soup = BeautifulSoup(response.data, 'html.parser')

    error_message = soup.find('div', {'class': 'alert alert-danger'})
    assert error_message.get_text() in exception_content
