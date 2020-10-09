#!/usr/bin/python3

# config.py
# Date: 09/10/2020
# Author: Laurentiu Mandru
# Email: mclaurentiu79@gmail.com

"""
Project wide configuration file.
"""

import os

RDFUNIT_QUERY_DELAY_MS = os.environ.get('RDFUNIT_QUERY_DELAY_MS', 1)
