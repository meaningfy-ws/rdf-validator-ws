#!/usr/bin/python3

# run_dev.py
# Date:  01/10/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com

"""
Development API server through connexion definitions.
"""

from validator.entrypoints.api import app
from validator.entrypoints.flask_config import DevelopmentConfig

app.config.from_object(DevelopmentConfig())

if __name__ == '__main__':
    app.run()
