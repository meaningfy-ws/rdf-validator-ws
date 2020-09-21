#!/usr/bin/python3

# service.py
# Date:  21/09/2020
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com 

""" """
from pathlib import Path


def run_validator(inputs, output: Path) -> None:
    """
        Execute the RDF Unit or any other validator.
        Possibilities: upload output to a SPARQL endpoint, or write it into a file.
    :param output:
    :type inputs: object
    :return:
    """


def generate_validation_report(path_to_report: Path, output: Path) -> None:
    """
        Generate the jinja HTML report.
        Warning: we have to decide what will be the report sources.
        Possibilities: (a) either write a new DataSourceAdapter in the eds4jinja project or
                       (b) use a temporary Fuseki instance,w here the validation report is
                       loaded and the report is generated from there.  (For this we have to write a Fuseki adapter)
    :param output:
    :param path_to_report:
    :return:
    """
