#
# This file is part of Python Client Library for STAC.
# Copyright (C) 2019 INPE.
#
# Python Client Library for STAC is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Unit-test for STAC operations."""

import os

from stac import stac

url =  os.environ.get('STAC_SERVER_URL', 'http://localhost')


def test_creation():
    service = stac(url)

    assert url.count(service.url) == 1


def test_conformance():
    service = stac(url)

    retval = service.conformance()

    assert 'conformsTo' in retval


def test_catalog():
    service = stac(url)

    retval = service.catalog()

    common_keys = { 'stac_version', 'id', 'description', 'links' }

    assert  common_keys <= set(retval.keys())

