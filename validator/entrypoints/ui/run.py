#!/usr/bin/python3

# run.py
# Date:  24/09/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com

"""
Production UI server through flask definitions.
"""
from validator.entrypoints.flask_config import ProductionConfig
from . import app

app.config.from_object(ProductionConfig())

if __name__ == '__main__':
    app.run()
