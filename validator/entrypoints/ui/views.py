#!/usr/bin/python3

# views.py
# Date:  24/09/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com

"""
UI pages

"""
import tempfile
from json import loads
from pathlib import Path

from flask import render_template, flash, send_from_directory

from validator.entrypoints.ui import app
from validator.entrypoints.ui.api_wrapper import validate_file as api_validate_file, \
    validate_sparql_endpoint as api_validate_sparql_endpoint
from validator.entrypoints.ui.forms import ValidateFromFileForm, ValidateSPARQLEndpointForm


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/validate-file', methods=['GET', 'POST'])
def validate_file():
    form = ValidateFromFileForm()

    if form.validate_on_submit():
        response, status = api_validate_file(
            dataset_uri=form.dataset_uri.data,
            data_file=form.data_file.data,
            schema_file=form.schema_file.data
        )

        if status != 200:
            flash(loads(response).get('detail'), 'error')
        else:
            with tempfile.TemporaryDirectory() as temp_folder:
                report = Path(temp_folder) / str('report.ttl')
                report.write_bytes(response)
                return send_from_directory(Path(temp_folder), 'report.ttl', as_attachment=True)

    return render_template('validate/file.html', form=form, title='Validate File')


@app.route('/validate-sparql-endpoint', methods=['GET', 'POST'])
def validate_sparql_endpoint():
    form = ValidateSPARQLEndpointForm()
    if form.validate_on_submit():
        response, status = api_validate_sparql_endpoint(
            dataset_uri=form.dataset_uri.data,
            sparql_endpoint_url=form.endpoint_url.data,
            schema_file=form.schema_file.data,
            graphs=form.graphs.data.split()
        )

        if status != 200:
            flash(loads(response).get('detail'), 'error')
        else:
            with tempfile.TemporaryDirectory() as temp_folder:
                report = Path(temp_folder) / str('report.ttl')
                report.write_bytes(response)
                return send_from_directory(Path(temp_folder), 'report.ttl', as_attachment=True)

    return render_template('validate/sparql_endpoint.html', form=form, title='Validate SPARQL Endpoint')
