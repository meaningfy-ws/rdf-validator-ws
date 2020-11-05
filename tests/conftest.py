#!/usr/bin/python3

# conftest.py
# Date:  01/10/2020
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com

"""
Fixtures and config data for the testing module.
"""
import pytest

from validator.entrypoints.api import app as api_app
from validator.entrypoints.ui import app as ui_app
from validator.config import TestingConfig


@pytest.fixture
def api_client():
    api_app.config.from_object(TestingConfig())
    return api_app.test_client()


@pytest.fixture
def ui_client():
    ui_app.config.from_object(TestingConfig())
    return ui_app.test_client()
