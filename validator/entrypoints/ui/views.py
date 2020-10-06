#!/usr/bin/python3

# views.py
# Date:  24/09/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com

"""
UI pages

"""
from flask import render_template

from . import app


@app.route('/')
def index():
    return render_template('index.html')