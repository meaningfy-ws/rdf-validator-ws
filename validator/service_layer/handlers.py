#!/usr/bin/python3

# service.py
# Date:  21/09/2020
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com 

""" """
import logging
from pathlib import Path
from typing import List

from validator.adapters.validator_wrapper import AbstractValidatorWrapper, RDFUnitWrapper

logger = logging.getLogger(__name__)


def run_file_validator(dataset_uri: str, data_file: str, schemas: List[str], output: Path) -> None:
    """
        Execute the RDF Unit or any other validator.
        Possibilities: upload output to a SPARQL endpoint, or write it into a file.
    :param data_file:
    :param schemas:
    :param data_files:
    :param dataset_uri:
    :param output:
    :type inputs: object
    :return:
    """
    # what test data should we use:
    # see tests/test-data/rdfunit-example and itb-example; the output reports might have problems
    if dataset_uri != data_file:
        logger.fatal("dataset_uri must the same as data_file")
        raise Exception("dataset_uri must the same as data_file")

    logging.info("RDFUnitWrapper' starting ...")
    validator_wrapper: AbstractValidatorWrapper
    validator_wrapper = RDFUnitWrapper("docker")
    cli_output = validator_wrapper.execute_subprocess("run", "aksw/rdfunit",
                                                      " -d ", dataset_uri,
                                                      " -u ", data_file,
                                                      " -s ", ", ".join([schema for schema in schemas]),
                                                      " -f ", str(output))
    logging.info("RDFUnitWrapper finished with output:\n" + cli_output)


def run_endpoint_validator(dataset_uri: str, graphs_uris: List[str], schemas: List[str], output: Path) -> None:
    """
        Execute the RDF Unit or any other validator.
        Possibilities: upload output to a SPARQL endpoint, or write it into a file.
    :param graphs_uris:
    :param dataset_uri:
    :param schemas:
    :param output:
    :type inputs: object
    :return:
    """
    # what test data should we use:
    # see tests/test-data/rdfunit-example and itb-example; the output reports might have problems

    logging.info("RDFUnitWrapper' starting ...")
    validator_wrapper: AbstractValidatorWrapper
    validator_wrapper = RDFUnitWrapper("docker")

    cli_output = validator_wrapper.execute_subprocess("run", "aksw/rdfunit",
                                                      " -d ", dataset_uri,
                                                      "" if (len(graphs_uris) is 0) else " -g ",
                                                      "" if (len(graphs_uris) is 0) else ", ".join([graph for graph in graphs_uris]),
                                                      " -s " + ", ".join(
                                                          [schema for schema in schemas]),
                                                      " -f " + str(output)
                                                      )
    logging.info("RDFUnitWrapper finished with output:\n" + cli_output)


def run_sparql_endpoint_validator(dataset_uri: str, sparql_endpoint_uri: str, graphs_uris: List[str],
                                  schemas: List[str], output: Path) -> None:
    """
        Execute the RDF Unit or any other validator.
        Possibilities: upload output to a SPARQL endpoint, or write it into a file.
    :param sparql_endpoint_uri:
    :param dataset_uri:
    :param graphs_uris:
    :param schemas:
    :param output:
    :type inputs: object
    :return:
    """
    # what test data should we use:
    # see tests/test-data/rdfunit-example and itb-example; the output reports might have problems

    logging.info("RDFUnitWrapper' starting ...")
    validator_wrapper: AbstractValidatorWrapper
    validator_wrapper = RDFUnitWrapper("docker")
    cli_output = validator_wrapper.execute_subprocess("run", "aksw/rdfunit",
                                                      " -d ",  dataset_uri,
                                                      " -e ", sparql_endpoint_uri,
                                                      "" if (len(graphs_uris) is 0) else " -g ",
                                                      "" if (len(graphs_uris) is 0) else ", ".join([graph for graph in graphs_uris]),
                                                      " -s ", ", ".join([schema for schema in schemas]),
                                                      " -f ",  str(output))
    logging.info("RDFUnitWrapper finished with output:\n" + cli_output)


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
