#!/usr/bin/python3

# run.py
# Date:  24/09/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com

"""
API server through connexion definitions
"""

import connexion

connexion_app = connexion.FlaskApp(__name__, specification_dir='openapi')
connexion_app.add_api('openapi.yaml')

app = connexion_app.app

if __name__ == '__main__':
    app.run()
