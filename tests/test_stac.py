#
# This file is part of Python Client Library for STAC.
# Copyright (C) 2019 INPE.
#
# Python Client Library for STAC is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Unit-test for STAC operations."""

import os
import unittest
from unittest.mock import patch


from stac import STAC

url =  os.environ.get('STAC_SERVER_URL', 'http://brazildatacube.dpi.inpe.br/bdc-stac/0.8.0')

def test_creation():
    service = STAC(url)

    assert url.count(service.url) == 1


def test_conformance():
    service = STAC(url)

    retval = service.conformance()

    assert 'conformsTo' in retval


def test_catalog():
    service = STAC(url)

    retval = service.catalog()

    common_keys = { 'stac_version', 'id', 'description', 'links' }

    assert  common_keys <= set(retval.keys())


# TODO: Mock API using unittest.mock.patch and json schemas
class TestSTAC(unittest.TestCase):
    def setUp(self):
        self.service = STAC(url)

    def test_collection(self):
        collection_name = 'S10mMEDIAN'

        res = self.service.collection(collection_name)

        self.assertEqual(res['id'], collection_name)
        self.assertIn('properties', res)
        self.assertIn('links', res)
        self.assertIn('stac_version', res)

    def test_collection_not_found(self):
        # TODO: Service collection should not throw too abroad exception
        with self.assertRaises(Exception) as e:
            self.service.collection('UnknownCollection')