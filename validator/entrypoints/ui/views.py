#!/usr/bin/python3

# views.py
# Date:  24/09/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com

"""
UI pages

"""
from flask import render_template

from validator.entrypoints.ui import app
from validator.entrypoints.ui.forms import ValidateFromFileForm, ValidateSPARQLEndpointForm


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/validate-file', methods=['GET', 'POST'])
def validate_file():
    form = ValidateFromFileForm()
    if form.validate_on_submit():
        print(form)
    return render_template('validate/file.html', form=form, title='Validate File')


@app.route('/validate-sparql-endpoint', methods=['GET', 'POST'])
def validate_sparql_endpoint():
    form = ValidateSPARQLEndpointForm()
    if form.validate_on_submit():
        print(form)
    return render_template('validate/sparql_endpoint.html', form=form, title='Validate SPARQL Endpoint')
