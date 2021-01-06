#!/usr/bin/python3

# test_service_layer_helpers.py
# Date:  06/01/2021
# Author: Mihai Coșleț
# Email: coslet.mihai@gmail.com
import pytest

from validator.service_layer.helpers import get_custom_shacl_shape_files, SHACLShapesMissing


def test_get_custom_shacl_shape_files_path_specified(tmpdir, monkeypatch):
    shapes_location = tmpdir.mkdir('shacl_shapes')
    shape1 = shapes_location.join('shape1.ttl')
    shape1.write('')
    shape2 = shapes_location.join('shape2.ttl')
    shape2.write('')

    monkeypatch.setenv('RDF_VALIDATOR_SHACL_SHAPES_PATH', str(shapes_location))

    shape_files = get_custom_shacl_shape_files()

    assert {str(shape1), str(shape2)} == set(shape_files)


def test_get_custom_shacl_shape_files_no_path_specified(monkeypatch):
    monkeypatch.delenv('RDF_VALIDATOR_SHACL_SHAPES_PATH', raising=False)

    assert not get_custom_shacl_shape_files()


def test_get_custom_shacl_shape_files_path_specified_no_files(tmpdir, monkeypatch):
    shapes_location = tmpdir.mkdir('shacl_shapes')
    monkeypatch.setenv('RDF_VALIDATOR_SHACL_SHAPES_PATH', str(shapes_location))

    with pytest.raises(SHACLShapesMissing) as e:
        _ = get_custom_shacl_shape_files()

    assert f'No SHACL shape files found at {shapes_location}' in str(e.value)
