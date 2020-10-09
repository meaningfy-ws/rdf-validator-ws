#!/usr/bin/python3

# helpers.py
# Date:  01/10/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com

"""
Helper methods

"""

from rdflib.util import guess_format

INPUT_MIME_TYPES = {
    'rdf': 'application/rdf+xml',
    'trix': 'application/xml',
    'nq': 'application/n-quads',
    'nt': 'application/n-triples',
    'jsonld': 'application/ld+json',
    'n3': 'text/n3',
    'ttl': 'text/turtle',
}

HTML_EXTENSION = 'html'
TTL_EXTENSION = 'ttl'
ZIP_EXTENSION = 'zip'

REPORT_EXTENSIONS = [TTL_EXTENSION, HTML_EXTENSION, ZIP_EXTENSION]
DEFAULT_REPORT_EXTENSION = REPORT_EXTENSIONS[0]


def _guess_file_type(file: str, accepted_types: dict = None):
    if accepted_types is None:
        accepted_types = INPUT_MIME_TYPES
    return guess_format(str(file), accepted_types)
