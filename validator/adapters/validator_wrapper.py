#!/usr/bin/python3

# rdfunit_wrapper.py
# Date:  21/09/2020
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com 

""" This module implements wrappers around a external RDF validation tools. """

import abc
import logging
from subprocess import Popen, PIPE


class SubprocessFailure(Exception):
    """
        An exception for SKOSHistoryRunner.
    """


class AbstractValidatorWrapper(abc.ABC):
    __FULL_PATH_TO_SCRIPT__: str

    @abc.abstractmethod
    def __init__(self, full_path_to_script):
        self.__FULL_PATH_TO_SCRIPT__ = full_path_to_script

    @abc.abstractmethod
    def run(self, *args):
        pass

    def execute_subprocess(self, *args):
        logging.info('Subprocess starting: ' + self.__FULL_PATH_TO_SCRIPT__)

        process = Popen(
            [self.__FULL_PATH_TO_SCRIPT__, args],
            stdout=PIPE)
        output, _ = process.communicate()

        if process.returncode != 0:
            logging.fatal('Subprocess failed: ' + self.__FULL_PATH_TO_SCRIPT__)
            logging.fatal(f'Subprocess: {output.decode()}')
            raise SubprocessFailure(output)

        logging.info('Subprocess finished successfully: ' + self.__FULL_PATH_TO_SCRIPT__)
        return output.decode()


class RDFUnitWrapper(AbstractValidatorWrapper):

    def __init__(self, full_path_to_script):
        super().__init__(full_path_to_script)

    def run(self, *args):
        self.execute_subprocess(args)
