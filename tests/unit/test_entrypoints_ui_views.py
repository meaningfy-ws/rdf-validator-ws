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
    response = client.get(url, follow_redirects=True)
    return BeautifulSoup(response.data, 'html.parser')


def test_index(ui_client):
    ui_url = '/'
    soup = _helper_get_request_and_parse(ui_client, ui_url)

    title = soup.find(id='title')
    assert 'Validate File' in title.get_text()


def test_custom_ui_name(ui_client, monkeypatch):
    ui_url = '/'
    monkeypatch.setenv('RDF_VALIDATOR_UI_NAME', 'Custom Validator')

    soup = _helper_get_request_and_parse(ui_client, ui_url)

    name = soup.find(id='website-name')
    assert 'Custom Validator' in name.get_text()


@patch('validator.entrypoints.ui.views.api_validate_file')
def test_validate_file(mock_api_validate_file, ui_client):
    ui_url = '/validate-file'
    mock_api_validate_file.return_value = RequestResponse(b'report file content', 200)

    soup = _helper_get_request_and_parse(ui_client, ui_url)

    title = soup.find(id='title')
    assert 'Validate File' in title.get_text()

    data = {
        'data_file': FileStorage(BytesIO(b'data file content'), 'data.rdf'),
        'schema_file': FileStorage(BytesIO(b'schema file content'), 'schema.rdf'),
        'report_extension': 'ttl'
    }

    response = ui_client.post('/validate-file', data=data, follow_redirects=True,
                              content_type='multipart/form-data')

    assert response.status_code == 200
    assert b'report file content' == response.data


@patch('validator.entrypoints.ui.views.api_validate_file')
def test_validate_file_type_exception(mock_api_validate_file, ui_client):
    ui_url = '/validate-file'
    exception_content = 'This file type is not supported'
    exception_response = {
        'detail': exception_content
    }
    mock_api_validate_file.return_value = dumps(exception_response), 415

    data = {
        'data_file': FileStorage(BytesIO(b'data file content'), 'data.pdf'),
        'schema_file': FileStorage(BytesIO(b'schema file content'), 'schema.pdf'),
        'report_extension': 'ttl'
    }

    response = ui_client.post(ui_url, data=data, follow_redirects=True,
                              content_type='multipart/form-data')
    soup = BeautifulSoup(response.data, 'html.parser')

    error_message = soup.find('div', {'class': 'card red lighten-3'})
    assert exception_content in error_message.get_text()


@patch('validator.entrypoints.ui.views.api_validate_sparql_endpoint')
def test_validate_sparql_endpoint(mock_api_validate_sparql_endpoint, ui_client):
    ui_url = '/validate-sparql-endpoint'
    mock_api_validate_sparql_endpoint.return_value = RequestResponse(b'schema file content', 200)

    soup = _helper_get_request_and_parse(ui_client, ui_url)

    title = soup.find(id='title')
    assert 'Validate SPARQL Endpoint' in title.get_text()

    data = {
        'endpoint_url': 'http://endpoint.url',
        'schema_file': FileStorage(BytesIO(b'schema file content'), 'schema.rdf'),
        'graphs': 'graph1 graph2',
        'report_extension': 'ttl'
    }

    response = ui_client.post(ui_url, data=data,
                              content_type='multipart/form-data')

    assert response.status_code == 200
    assert b'schema file content' == response.data


@patch('validator.entrypoints.ui.views.api_validate_sparql_endpoint')
def test_validate_sparql_endpoint_type_exception(mock_api_validate_sparql_endpoint, ui_client):
    ui_url = '/validate-sparql-endpoint'
    exception_content = 'This file type is not supported'
    exception_response = {
        'detail': exception_content
    }
    mock_api_validate_sparql_endpoint.return_value = dumps(exception_response), 415

    data = {
        'endpoint_url': 'http://endpoint.url',
        'schema_file': FileStorage(BytesIO(b'schema file content'), 'schema.rdf'),
        'graphs': 'graph1 graph2',
        'report_extension': 'ttl'
    }

    response = ui_client.post(ui_url, data=data, follow_redirects=True,
                              content_type='multipart/form-data')
    soup = BeautifulSoup(response.data, 'html.parser')

    error_message = soup.find('div', {'class': 'card red lighten-3'})
    assert exception_content in error_message.get_text()
