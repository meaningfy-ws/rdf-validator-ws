#!/usr/bin/python3

# run_dev.py
# Date:  01/10/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com

"""
Development UI server through flask definitions.

"""
from validator.entrypoints.ui import app
from validator.entrypoints.manage import DevelopmentConfig

app.config.from_object(DevelopmentConfig())

if __name__ == '__main__':
    app.run()
