#!/usr/bin/python3

# service.py
# Date:  21/09/2020
# Author: Laurentiu Mandru
# Email: mclaurentiu79@gmail.com

""" """
import logging
import pathlib
from distutils.dir_util import copy_tree
from pathlib import Path
from typing import List
from urllib.parse import urlparse

from eds4jinja2.builders.report_builder import ReportBuilder

from validator.adapters.validator_wrapper import AbstractValidatorWrapper, RDFUnitWrapper

__logger = logging.getLogger(__name__)


def __copy_static_content(from_path, to_path):
    if pathlib.Path(from_path).is_dir():
        copy_tree(from_path, to_path)
    else:
        __logger.warning(from_path + " is not a directory !")


def run_file_validator(dataset_uri: str, data_file: str, schemas: List[str], output: Path) -> str:
    """
        Execute the RDF Unit or any other validator.
        Possibilities: upload output to a SPARQL endpoint, or write it into a file.
    :type schemas: object
    :param data_file: defines the actual location of the file
    :param schemas: schemas also required for running an evaluation
    :param dataset_uri: states a URI that relates to the tested dataset
    :param output: the output directory
    :return: nothing

    Please see https://github.com/AKSW/RDFUnit/wiki/CLI for a comprehensive description of the parameters
    """
    if dataset_uri != data_file:
        __logger.fatal("dataset_uri must be the same as data_file")
        raise Exception("dataset_uri must be the same as data_file")

    __logger.info("RDFUnitWrapper starting ...")
    validator_wrapper: AbstractValidatorWrapper
    validator_wrapper = RDFUnitWrapper("java")
    cli_output = validator_wrapper.execute_subprocess("-jar", "/usr/src/app/rdfunit-validate.jar",
                                                      " -d ", dataset_uri,
                                                      " -u ", data_file,
                                                      " -s ", ", ".join([schema for schema in schemas]),
                                                      " -f ", str(output))
    __logger.info("RDFUnitWrapper finished with output:\n" + cli_output)
    return Path(output) / "results" / (data_file + ".shaclTestCaseResult.html")


def run_endpoint_validator(dataset_uri: str, graphs_uris: List[str], schemas: List[str], output: Path) -> str:
    """
        Execute the RDF Unit or any other validator.
        Possibilities: upload output to a SPARQL endpoint, or write it into a file.
    :param graphs_uris: the URIs of the graphs
    :param dataset_uri: states a URI that relates to the tested dataset
    :param schemas: schemas also required for running an evaluation
    :param output: the output directory
    :return: nothing

    Please see https://github.com/AKSW/RDFUnit/wiki/CLI for a comprehensive description of the parameters
    """

    __logger.info("RDFUnitWrapper' starting ...")
    validator_wrapper: AbstractValidatorWrapper
    validator_wrapper = RDFUnitWrapper("java")

    cli_output = validator_wrapper.execute_subprocess("-jar", "/usr/src/app/rdfunit-validate.jar",
                                                      " -d ", dataset_uri,
                                                      "" if (len(graphs_uris) == 0) else " -g " + ", ".join(
                                                          [graph for graph in graphs_uris]),
                                                      " -s " + ", ".join(
                                                          [schema for schema in schemas]),
                                                      " -f " + str(output)
                                                      )
    __logger.info("RDFUnitWrapper finished with output:\n" + cli_output)

    parsed_uri = urlparse(dataset_uri)
    output_file_name = parsed_uri.netloc.replace(":", "_") + \
                       parsed_uri.path.replace("/", "_") + \
                       ".shaclTestCaseResult.html"

    return Path(output) / "results" / output_file_name


def run_sparql_endpoint_validator(dataset_uri: str, sparql_endpoint_uri: str, graphs_uris: List[str],
                                  schemas: List[str], output: Path) -> str:
    """
        Execute the RDF Unit or any other validator.
        Possibilities: upload output to a SPARQL endpoint, or write it into a file.
    :param sparql_endpoint_uri: You can run RDFUnit directly on a SPARQL endpoint using this parameter
    :param dataset_uri: states a URI that relates to the tested dataset
    :param graphs_uris: the URIs of the graphs
    :param schemas: schemas also required for running an evaluation
    :param output: the output directory
    :return: nothing

    Please see https://github.com/AKSW/RDFUnit/wiki/CLI for a comprehensive description of the parameters
    """

    __logger.info("RDFUnitWrapper' starting ...")
    validator_wrapper: AbstractValidatorWrapper
    validator_wrapper = RDFUnitWrapper("java")
    cli_output = validator_wrapper.execute_subprocess("-jar", "/usr/src/app/rdfunit-validate.jar",
                                                      " -d ", dataset_uri,
                                                      " -e ", sparql_endpoint_uri,
                                                      "" if (len(graphs_uris) == 0) else " -g " + ", ".join(
                                                          [graph for graph in graphs_uris]),
                                                      " -s ", ", ".join([schema for schema in schemas]),
                                                      " -f ", str(output))
    __logger.info("RDFUnitWrapper finished with output:\n" + cli_output)

    parsed_uri = urlparse(dataset_uri)
    output_file_name = parsed_uri.netloc.replace(":", "_") + \
                       parsed_uri.path.replace("/", "_") + \
                       ".shaclTestCaseResult.html"

    return Path(output) / "results" / output_file_name


def generate_validation_report(path_to_report: Path, output: Path) -> None:
    """
        Generate the jinja HTML report.
        Warning: we have to decide what will be the report sources.
        Possibilities: (a) either write a new DataSourceAdapter in the eds4jinja project or
                       (b) use a temporary Fuseki instance,w here the validation report is
                       loaded and the report is generated from there.  (For this we have to write a Fuseki adapter)
    :param output: the output directory
    :param path_to_report: the location of the template file(s) that will be used to render the output
    :return: nothing
    """

    report_builder = ReportBuilder(path_to_report, output)
    report_builder.add_after_rendering_listener(__copy_static_content)
    report_builder.make_document()
