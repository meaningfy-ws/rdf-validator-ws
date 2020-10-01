#!/usr/bin/python3

# forms.py
# Date:  24/09/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com

"""
    Form classes for use in views.

"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed

from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, URL


class BaseValidateForm(FlaskForm):
    dataset_uri = StringField('Dataset URI', validators=[URL()])
    schema_file = FileField('Schema file',
                            validators=[FileRequired(),
                                        FileAllowed(['ttl'], 'This rdf format is not supported')])
    submit = SubmitField('Validate')


class ValidateFromFileForm(BaseValidateForm):
    data_file = FileField('Data file',
                          validators=[FileRequired(),
                                      FileAllowed(['ttl'], 'This rdf format is not supported')])
    submit = SubmitField('Validate')


class ValidateSPARQLEndpointForm(BaseValidateForm):
    endpoint_url = StringField('Endpoint URL', validators=[DataRequired(), URL()])
    graphs = TextAreaField('Graphs', description='Separate them through spaces. example: graph1 graph2')
    submit = SubmitField('Validate')
