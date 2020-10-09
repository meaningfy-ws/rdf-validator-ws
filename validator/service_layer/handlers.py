#!/usr/bin/python3

# service.py
# Date:  21/09/2020
# Author: Laurentiu Mandru
# Email: mclaurentiu79@gmail.com

""" """
import json
import logging
from distutils.dir_util import copy_tree
from pathlib import Path
from typing import List, Union
from urllib.parse import urlparse

from eds4jinja2.builders.report_builder import ReportBuilder

from validator.adapters.validator_wrapper import AbstractValidatorWrapper, RDFUnitWrapper
from validator.config import RDFUNIT_QUERY_DELAY_MS

logger = logging.getLogger(__name__)


def __copy_static_content(from_path, to_path):
    if Path(from_path).is_dir():
        copy_tree(from_path, to_path)
    else:
        logger.warning(from_path + " is not a directory!")


def run_file_validator(data_file: str, schemas: List[str], output: Union[str, Path]) -> tuple:
    """
        Execute the RDF Unit or any other validator.
        Possibilities: upload output to a SPARQL endpoint, or write it into a file.
    :type schemas: object
    :param data_file: defines the actual location of the file
    :param schemas: schemas also required for running an evaluation
    :param output: the output directory
    :return: a tuple of the output file paths

    Please see https://github.com/AKSW/RDFUnit/wiki/CLI for a comprehensive description of the parameters
    """
    logger.info("RDFUnitWrapper starting ...")
    validator_wrapper: AbstractValidatorWrapper
    validator_wrapper = RDFUnitWrapper("java")
    cli_output = validator_wrapper.execute_subprocess("-jar", "/usr/src/rdfunit/rdfunit-validate.jar",
                                                      "-d", data_file,
                                                      "-u", data_file,
                                                      "-s", ", ".join([schema for schema in schemas]),
                                                      "-r", 'shacl',
                                                      "-o", 'html,ttl',
                                                      "-f", str(output))
    logger.info("RDFUnitWrapper finished with output:\n" + cli_output)

    output_file_name = str(Path(data_file).parent).replace('/', '_') + '_' + Path(
        data_file).name + ".shaclTestCaseResult"
    output_file_full_path = Path(output) / 'results' / output_file_name
    return str(output_file_full_path) + ".html", str(output_file_full_path) + ".ttl"


# def run_endpoint_validator(dataset_uri: str, graphs_uris: List[str], schemas: List[str], output: Path) -> str:
#     """
#         Execute the RDF Unit or any other validator.
#         Possibilities: upload output to a SPARQL endpoint, or write it into a file.
#     :param graphs_uris: the URIs of the graphs
#     :param dataset_uri: states a URI that relates to the tested dataset
#     :param schemas: schemas also required for running an evaluation
#     :param output: the output directory
#     :return: nothing
#
#     Please see https://github.com/AKSW/RDFUnit/wiki/CLI for a comprehensive description of the parameters
#     """
#
#     logger.info("RDFUnitWrapper' starting ...")
#     validator_wrapper: AbstractValidatorWrapper
#     validator_wrapper = RDFUnitWrapper("java")
#
#     cli_output = validator_wrapper.execute_subprocess("-jar", "/usr/src/app/rdfunit-validate.jar",
#                                                       "-d", dataset_uri,
#                                                       "" if (len(graphs_uris) == 0) else " -g " + ", ".join(
#                                                           [graph for graph in graphs_uris]),
#                                                       "-s" + ", ".join(
#                                                           [schema for schema in schemas]),
#                                                       "-r", 'shacl',
#                                                       "-o", 'html,ttl',
#                                                       "-f" + str(output)
#                                                       )
#     logger.info("RDFUnitWrapper finished with output:\n" + cli_output)
#
#     parsed_uri = urlparse(dataset_uri)
#     output_file_name = parsed_uri.netloc.replace(":", "_") + \
#                        parsed_uri.path.replace("/", "_") + \
#                        ".shaclTestCaseResult.html"
#
#     return Path(output) / "results" / output_file_name


def run_sparql_endpoint_validator(sparql_endpoint_url: str, graphs_uris: List[str],
                                  schemas: List[str], output: Union[str, Path]) -> tuple:
    """
        Execute the RDF Unit or any other validator.
        Possibilities: upload output to a SPARQL endpoint, or write it into a file.
    :param sparql_endpoint_url: You can run RDFUnit directly on a SPARQL endpoint using this parameter
    :param graphs_uris: the URIs of the graphs
    :param schemas: schemas also required for running an evaluation
    :param output: the output directory
    :return: a tuple of the output file paths

    Please see https://github.com/AKSW/RDFUnit/wiki/CLI for a comprehensive description of the parameters
    """

    logger.info("RDFUnitWrapper starting ...")
    validator_wrapper: AbstractValidatorWrapper
    validator_wrapper = RDFUnitWrapper("java")

    sparql_endpoint_url = sparql_endpoint_url.strip()

    if graphs_uris is None or len(graphs_uris) == 0:
        graph_param = ""
    else:
        graph_param = "-g" + ", ".join([graph for graph in graphs_uris])

    cli_output = validator_wrapper.execute_subprocess("-jar", "/usr/src/rdfunit/rdfunit-validate.jar",
                                                      "-d", sparql_endpoint_url,
                                                      "-e", sparql_endpoint_url,
                                                      graph_param,
                                                      "-s", ", ".join([schema for schema in schemas]),
                                                      "-r", 'shacl',
                                                      "-C", "-T", "0", "-D", str(RDFUNIT_QUERY_DELAY_MS),
                                                      "-o", 'html,ttl',
                                                      "-f", str(output))
    logger.info("RDFUnitWrapper finished with output:\n" + cli_output)

    parsed_uri = urlparse(sparql_endpoint_url)
    output_file_name = parsed_uri.netloc.replace(":", "_") + \
                       parsed_uri.path.replace("/", "_") + \
                       ".shaclTestCaseResult"
    output_file_path = Path(output) / 'results' / output_file_name
    return str(output_file_path) + ".html", str(output_file_path) + ".ttl"


def generate_validation_report(path_to_report: Union[str, Path]) -> str:
    """
        Generate the jinja HTML report.
        Warning: we have to decide what will be the report sources.
        Possibilities: (a) either write a new DataSourceAdapter in the eds4jinja project or
                       (b) use a temporary Fuseki instance,w here the validation report is
                       loaded and the report is generated from there.  (For this we have to write a Fuseki adapter)
    :param path_to_report: the location of the template file(s) that will be used to render the output
    :return: path to the html report
    """
    report_builder = ReportBuilder(path_to_report)
    report_builder.add_after_rendering_listener(__copy_static_content)
    report_builder.make_document()
    return str(path_to_report) + "/output/" + "main.html"


def prepare_eds4jinja_context(report_path, source_file):
    copy_tree("templates/rdfunit-shacl-report/", report_path)

    with open(Path(report_path) / "config.json", 'r+') as config_file:
        config = json.load(config_file)
        config["conf"]["report_data_file"] = source_file
        logger.info(config)
        config_file.seek(0)
        json.dump(config, config_file)
        config_file.truncate()
