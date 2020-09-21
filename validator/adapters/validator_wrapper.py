#!/usr/bin/python3

# rdfunit_wrapper.py
# Date:  21/09/2020
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com 

""" This module implements wrappers around a external RDF validation tools. """

import abc


class AbstractValidatorWrapper(abc.ABC):

    @abc.abstractmethod
    def run(self):
        pass

    def execute_subprocess(self):
        """
            TODO: implement subprocess execution in a generic way, +exception handling, then call it in the `run`
        :return:
        """


class RDFUnitWrapper(AbstractValidatorWrapper):

    def __init__(self):
        pass

    def run(self):
        pass
