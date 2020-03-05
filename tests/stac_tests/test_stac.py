#
# This file is part of Python Client Library for STAC.
# Copyright (C) 2019 INPE.
#
# Python Client Library for STAC is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Unit-test for STAC operations."""

import json
import os
import re

from pathlib import Path
from pkg_resources import resource_filename, resource_string

import pytest
import requests
import stac

url = os.environ.get('STAC_SERVER_URL', 'http://localhost')
match_url = re.compile(url)

class TestUtils:
    def test_ok(self, requests_mock):
        requests_mock.get(match_url, json={"key":"value"}, status_code=200, headers={'content-type':'application/json'})
        stac.Utils._get(url)

    def test_error(self, requests_mock):
        requests_mock.get(match_url, json={"key":"value"}, status_code=200, headers={'content-type':'text/plain'})
        with pytest.raises(ValueError):
            stac.Utils._get(url)

@pytest.fixture
def requests_mock(requests_mock):
    requests_mock.get(re.compile('https://geojson.org/'), real_http=True)
    yield requests_mock

@pytest.fixture(scope='session')
def stac_objects():
    directory = resource_filename(__name__, 'jsons/')
    files = dict()
    for path in Path(directory).rglob('*.json'):
        path = str(path)
        s = path.split('/')

        file_path = '/'.join(s[-3:])
        file = json.loads(resource_string(__name__, file_path))
        if s[-2] in files:
            files[s[-2]][s[-1]] = file
        else:
            files[s[-2]] = {s[-1]: file}

    return files

class TestStac:
    def test_stac(self):
        s = stac.STAC(url, True)
        assert s.url == url
        assert repr(s) == f'stac("{url}")'
        assert str(s) == f'<STAC [{url}]>'

    def test_catalog(self, stac_objects, requests_mock):
        for k in stac_objects:
            s = stac.STAC(url, True)

            requests_mock.get(match_url, json=stac_objects[k]['catalog.json'],
                              status_code=200,
                              headers={'content-type':'application/json'})

            response = s.catalog
            assert s._catalog.stac_version
            assert s._catalog.id
            assert s._catalog.description
            assert s._catalog.title
            assert s._catalog.links[0].type
            assert s._catalog.links[0].title
            assert s._catalog.links[0].href
            assert s._catalog.links[0].rel
            assert response == set(['my_collection1'])

    def test_collection(self, stac_objects, requests_mock):
        for k in stac_objects:
            s = stac.STAC(url, True)
            requests_mock.get(match_url, json=stac_objects[k]['catalog.json'],
                              status_code=200,
                              headers={'content-type':'application/json'})
            response = s.catalog

            requests_mock.get(match_url, json=stac_objects[k]['collection.json'],
                              status_code=200,
                              headers={'content-type':'application/json'})

            collection = s.collection('my_collection1')

            assert collection == stac_objects[k]['collection.json']
            assert collection.keywords
            assert collection.version
            assert collection.license
            assert collection.properties
            assert collection.providers[0].name
            assert collection.providers[0].description
            assert collection.providers[0].roles
            assert collection.providers[0].url
            if k == '0.8.0':
                assert collection.extent.spatial.bbox
                assert collection.extent.temporal.interval
                assert collection.summaries
                assert collection.summaries['val'].min == 0
                assert collection.summaries['val'].max == 1
            else:
                assert collection.extent.spatial
                assert collection.extent.temporal

    def test_collection_missing(self, stac_objects, requests_mock):
        for k in stac_objects:
            s = stac.STAC(url, True)
            requests_mock.get(match_url, json=stac_objects[k]['catalog.json'],
                              status_code=200,
                              headers={'content-type':'application/json'})
            response = s.catalog

            requests_mock.get(match_url,
                              exc=requests.exceptions.HTTPError)

            with pytest.raises(KeyError):
                s.collection('missing_collection')

    def test_collection_without_catalog(self, stac_objects, requests_mock):
        for k in stac_objects:
            s = stac.STAC(url, True)
            requests_mock.get(match_url, json=stac_objects[k]['collection.json'],
                              status_code=200,
                              headers={'content-type':'application/json'})
            response = s.collections

            assert s.collection('my_collection1') == stac_objects[k]['collection.json']

    def test_item(self, stac_objects, requests_mock):
        for k in stac_objects:
            s = stac.STAC(url, True)
            requests_mock.get(match_url, json=stac_objects[k]['catalog.json'],
                              status_code=200,
                              headers={'content-type':'application/json'})
            catalog = s.catalog

            requests_mock.get(match_url, json=stac_objects[k]['collection.json'],
                              status_code=200,
                              headers={'content-type':'application/json'})
            collection = s.collection('my_collection1')

            requests_mock.get(match_url, json=stac_objects[k]['items.json'],
                              status_code=200,
                              headers={'content-type':'application/json'})

            itemcollection = s.collection('my_collection1').get_items()
            item = itemcollection.features[0]

            if collection.stac_version == '0.8.0':
                assert itemcollection.links
                assert item.properties.datetime
                assert item.properties.license
                assert item.properties.providers
                assert item.properties.title
                assert item.properties.created
                assert item.properties.updated
            assert itemcollection.type
            assert item.id == 'feature1'
            assert item.stac_version
            assert item.type
            assert item.bbox
            assert item.collection
            assert item.geometry.type
            assert item.geometry.coordinates
            assert item.properties
            assert item.links
            assert item.assets['thumbnail'].href
            assert item.assets['thumbnail'].title
            assert item.assets['thumbnail'].type

    def test_item_id(self, stac_objects, requests_mock):
        for k in stac_objects:
            s = stac.STAC(url, True)
            requests_mock.get(match_url, json=stac_objects[k]['catalog.json'],
                              status_code=200,
                              headers={'content-type':'application/json'})
            response = s.catalog

            requests_mock.get(match_url, json=stac_objects[k]['collection.json'],
                              status_code=200,
                              headers={'content-type':'application/json'})
            response = s.collections

            requests_mock.get(match_url, json=stac_objects[k]['items.json']['features'][0],
                              status_code=200,
                              headers={'content-type':'application/json'})
            response = s.collection('my_collection1').get_items(item_id='feature1')

            assert response.id == 'feature1'

    def test_item_empty(self, stac_objects, requests_mock):
        for k in stac_objects:
            s = stac.STAC(url, True)
            requests_mock.get(match_url, json=stac_objects[k]['collection.json'],
                              status_code=200,
                              headers={'content-type':'application/json'})
            collection = s.collection('my_collection1')

            requests_mock.get(match_url, json=stac_objects[k]['items.json']['features'][0],
                              status_code=200,
                              headers={'content-type':'application/json'})
            collection['links'].pop(1)
            assert collection.get_items() == stac.ItemCollection({})

    def test_search(self, stac_objects, requests_mock):
        for k in stac_objects:
            s = stac.STAC(url, True)
            requests_mock.get(match_url, json=stac_objects[k]['collection.json'],
                              status_code=200,
                              headers={'content-type':'application/json'})
            response = s.collections

            requests_mock.get(match_url, json=stac_objects[k]['items.json'],
                              status_code=200,
                              headers={'content-type':'application/json'})

            response = s.search()

            assert response.features[0].id == 'feature1'

if __name__ == '__main__':
    pytest.main(['--color=auto', '--no-cov'])
