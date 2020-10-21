#!/usr/bin/python3

# test_service_layer_handers.py
# Date:  10/10/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com
from unittest.mock import patch

from validator.entrypoints.api.helpers import TTL_EXTENSION, HTML_EXTENSION, ZIP_EXTENSION
from validator.service_layer.handlers import create_report


def test_create_report_ttl(tmpdir):
    location = tmpdir.mkdir('location')
    html_report = 'report.html'
    ttl_report = 'report.ttl'
    extension = TTL_EXTENSION
    filename = 'filename'
    report_path, report_filename = create_report(location, html_report, ttl_report, extension, filename)

    assert report_path == ttl_report
    assert report_filename == 'filename-report.ttl'


@patch('validator.service_layer.handlers.prepare_eds4jinja_context')
@patch('validator.service_layer.handlers.generate_validation_report')
def test_create_report_html(mock_generate_validation_report, tmpdir):
    mock_generate_validation_report.return_value = '/report/location.html'

    location = tmpdir.mkdir('location')
    html_report = 'report.html'
    ttl_report = 'report.ttl'
    extension = HTML_EXTENSION
    filename = 'filename'
    report_path, report_filename = create_report(location, html_report, ttl_report, extension, filename)

    assert report_path == '/report/location.html'
    assert report_filename == 'filename-report.html'


@patch('validator.service_layer.handlers.prepare_eds4jinja_context')
@patch('validator.service_layer.handlers.generate_validation_report')
def test_create_report_zip(mock_generate_validation_report, mock_prepare_eds4jinja_context, tmpdir):
    shacl_html_report = tmpdir.join('shacl-report.html')
    shacl_html_report.write('shacl html report')
    html_report = tmpdir.join('report.html')

    mock_generate_validation_report.return_value = str(shacl_html_report)

    location = tmpdir.mkdir('location')
    html_report = tmpdir.join('report.html')
    html_report.write('html report')
    ttl_report = tmpdir.join('report.ttl')
    ttl_report.write('ttl report')
    extension = ZIP_EXTENSION
    filename = 'filename'

    report_path, report_filename = create_report(location, html_report, ttl_report, extension, filename)

    assert report_path == str(location) + '/report.zip'
    assert report_filename == 'filename-report.zip'