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

from wtforms import StringField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired, URL

from validator.entrypoints.api.helpers import HTML_EXTENSION, TTL_EXTENSION, ZIP_EXTENSION


class BaseValidateForm(FlaskForm):
    report_extension = RadioField('Report Extension', choices=[(TTL_EXTENSION, 'Turtle report'), (HTML_EXTENSION, 'HTML report'),
                                                               (ZIP_EXTENSION, 'Both reports')])
    schema_file = FileField('Schema file*',
                            validators=[FileRequired()])
    submit = SubmitField('Validate')


class ValidateFromFileForm(BaseValidateForm):
    data_file = FileField('Data file*',
                          validators=[FileRequired()])


class ValidateSPARQLEndpointForm(BaseValidateForm):
    endpoint_url = StringField('Endpoint URL*', validators=[DataRequired()])
    graphs = TextAreaField('Graphs', description='Separate them through spaces. example: graph1 graph2')
