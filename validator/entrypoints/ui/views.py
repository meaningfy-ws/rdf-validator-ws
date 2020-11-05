#!/usr/bin/python3

# views.py
# Date:  24/09/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com

"""
UI pages

"""
import tempfile
from pathlib import Path

from flask import render_template, flash, send_from_directory, redirect, url_for

from validator.entrypoints.api.helpers import TTL_EXTENSION
from validator.entrypoints.ui import app
from validator.entrypoints.ui.api_wrapper import validate_file as api_validate_file, \
    validate_sparql_endpoint as api_validate_sparql_endpoint
from validator.entrypoints.ui.forms import ValidateFromFileForm, ValidateSPARQLEndpointForm
from validator.entrypoints.ui.helpers import get_error_message_from_response


@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('validate_file'))


@app.route('/validate-file', methods=['GET', 'POST'])
def validate_file():
    form = ValidateFromFileForm()

    if form.validate_on_submit():
        response, status = api_validate_file(
            report_extension=form.report_extension.data,
            data_file=form.data_file.data,
            schema_files=form.schema_files.data
        )

        if status != 200:
            flash(get_error_message_from_response(response), 'error')
        else:
            report_extension = form.report_extension.data if form.report_extension.data else TTL_EXTENSION

            with tempfile.TemporaryDirectory() as temp_folder:
                report = Path(temp_folder) / str(f'report.{report_extension}')
                report.write_bytes(response)
                return send_from_directory(Path(temp_folder), f'report.{report_extension}', as_attachment=True)

    return render_template('validate/file.html', form=form, title='Validate File')


@app.route('/validate-sparql-endpoint', methods=['GET', 'POST'])
def validate_sparql_endpoint():
    form = ValidateSPARQLEndpointForm()

    if form.validate_on_submit():
        response, status = api_validate_sparql_endpoint(
            report_extension=form.report_extension.data,
            sparql_endpoint_url=form.endpoint_url.data,
            schema_files=form.schema_files.data,
            graphs=form.graphs.data.split()
        )

        if status != 200:
            flash(get_error_message_from_response(response), 'error')
        else:
            report_extension = form.report_extension.data if form.report_extension.data else TTL_EXTENSION

            with tempfile.TemporaryDirectory() as temp_folder:
                report = Path(temp_folder) / str(f'report.{report_extension}')
                report.write_bytes(response)
                return send_from_directory(Path(temp_folder), f'report.{report_extension}', as_attachment=True)

    return render_template('validate/sparql_endpoint.html', form=form, title='Validate SPARQL Endpoint')
