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

import pytest
import requests
from click.testing import CliRunner
from pkg_resources import resource_filename, resource_string

import stac

url = os.environ.get('STAC_SERVER_URL', 'http://localhost')
match_url = re.compile(url)



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

@pytest.fixture(scope='module')
def runner():
    return CliRunner()

class TestUtils:
    def test_ok(self, requests_mock):
        requests_mock.get(match_url, json={"key":"value"}, status_code=200, headers={'content-type':'application/json'})
        stac.Utils._get(url)

    def test_error(self, requests_mock):
        requests_mock.get(match_url, json={"key":"value"}, status_code=200, headers={'content-type':'text/plain'})
        with pytest.raises(ValueError):
            stac.Utils._get(url)



class TestStac:
    def test_stac(self):
        s = stac.STAC(url, True)
        assert s.url == url
        assert repr(s) == f'stac("{url}")'
        assert str(s) == f'<STAC [{url}]>'

    def test_catalog(self, stac_objects, requests_mock):
        for k in stac_objects:
            s = stac.STAC(url + "/stac" if k != '0.9.0' else url, True)

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
            assert response == ['my_collection1']

    def test_collections(self, stac_objects, requests_mock):
        for k in stac_objects:
            s = stac.STAC(url + "/stac" if k != '0.9.0' else url, True)
            requests_mock.get(match_url,
                              json=dict(collections=[stac_objects[k]['collection.json']]),
                              status_code=200,
                              headers={'content-type':'application/json'})

            response = s.collections
            assert response['my_collection1']

    def test_collection(self, stac_objects, requests_mock):
        for k in stac_objects:
            s = stac.STAC(url + "/stac" if k != '0.9.0' else url, True)
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
            if k == '0.7.0':
                assert collection.extent.spatial
                assert collection.extent.temporal
            else:
                assert collection.extent.spatial.bbox
                assert collection.extent.temporal.interval
                assert collection.summaries
                assert collection.summaries['val'].min == 0
                assert collection.summaries['val'].max == 1

    def test_collection_missing(self, stac_objects, requests_mock):
        for k in stac_objects:
            s = stac.STAC(url + "/stac" if k != '0.9.0' else url, True)
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
            s = stac.STAC(url + "/stac" if k != '0.9.0' else url, True)
            requests_mock.get(match_url, json=stac_objects[k]['collection.json'],
                              status_code=200,
                              headers={'content-type':'application/json'})
            response = s.collection('my_collection1')

            assert response == stac_objects[k]['collection.json']

    def test_item(self, stac_objects, requests_mock):
        for k in stac_objects:
            s = stac.STAC(url + "/stac" if k != '0.9.0' else url, True)
            if k == '0.9.0':
                requests_mock.get(re.compile(url+'/'), json=stac_objects[k]['catalog.json'],
                              status_code=200,
                              headers={'content-type':'application/json'})

            else:
                requests_mock.get(re.compile(url+'/stac'), json=stac_objects[k]['catalog.json'],
                              status_code=200,
                              headers={'content-type':'application/json'})
            catalog = s.catalog

            s.catalog #test for non empty catalog

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
            s = stac.STAC(url + "/stac" if k != '0.9.0' else url, True)
            requests_mock.get(match_url, json=stac_objects[k]['catalog.json'],
                              status_code=200,
                              headers={'content-type':'application/json'})
            response = s.catalog

            requests_mock.get(match_url, json=stac_objects[k]['collection.json'],
                              status_code=200,
                              headers={'content-type':'application/json'})
            collection = s.collection('my_collection1')

            requests_mock.get(match_url, json=stac_objects[k]['items.json']['features'][0],
                              status_code=200,
                              headers={'content-type':'application/json'})
            response = collection.get_items(item_id='feature1')

            assert response.id == 'feature1'

    def test_item_empty(self, stac_objects, requests_mock):
        for k in stac_objects:
            s = stac.STAC(url + "/stac" if k != '0.9.0' else url, True)
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
            s = stac.STAC(url + "/stac" if k != '0.9.0' else url, True)

            requests_mock.get(match_url, json=stac_objects[k]['catalog.json'],
                              status_code=200,
                              headers={'content-type':'application/json'})

            response = s.catalog

            requests_mock.get(match_url, json=stac_objects[k]['items.json'],
                              status_code=200,
                              headers={'content-type':'application/json'})

            response = s.search()

            assert response.features[0].id == 'feature1'

    def test_empty_bbox(self, stac_objects, requests_mock):
        for k in stac_objects:
            s = stac.STAC(url + "/stac" if k != '0.9.0' else url, True)

            requests_mock.get(match_url, json=stac_objects[k]['catalog.json'],
                              status_code=200,
                              headers={'content-type':'application/json'})

            with pytest.raises(TypeError):
                s.search(filter={"bbox": ""})

            with pytest.raises(TypeError):
                s.search(filter={"bbox": -90})

class TestCli:
    def test_catalog(self, stac_objects, requests_mock, runner):
        for k in stac_objects:
            requests_mock.get(match_url, json=stac_objects[k]['catalog.json'],
                              status_code=200,
                              headers={'content-type':'application/json'})

            result = runner.invoke(stac.cli.catalog, ['--url', url + "/stac" if k != '0.9.0' else url])
            assert result.exit_code == 0
            assert 'my_collection1' in result.output

    def test_collection(self, stac_objects, requests_mock, runner):
        for k in stac_objects:
            requests_mock.get(re.compile(url + "/stac" if k != '0.9.0' else url),
                              json=stac_objects[k]['catalog.json'],
                              status_code=200,
                              headers={'content-type':'application/json'})

            requests_mock.get(re.compile(url+'/collections'), json=stac_objects[k]['collection.json'],
                              status_code=200,
                              headers={'content-type':'application/json'})

            result = runner.invoke(stac.cli.collection, ['--url', url + "/stac" if k != '0.9.0' else url,
                                                          '--collection-id', 'my_collection1'])
            assert result.exit_code == 0
            assert 'my_collection1' in result.output

    def test_items(self, stac_objects, requests_mock, runner):
        for k in stac_objects:

            requests_mock.get(re.compile(url + "/stac" if k != '0.9.0' else url+'/'), json=stac_objects[k]['catalog.json'],
                              status_code=200,
                              headers={'content-type':'application/json'})

            requests_mock.get(re.compile(url+'/collections'), json=stac_objects[k]['collection.json'],
                              status_code=200,
                              headers={'content-type':'application/json'})

            requests_mock.get(re.compile(url+'/collections/my_collection1/items'), json=stac_objects[k]['items.json'],
                              status_code=200,
                              headers={'content-type':'application/json'})

            result = runner.invoke(stac.cli.items, ['--url', url + "/stac" if k != '0.9.0' else url,
                                                    '--collection-id', 'my_collection1',
                                                    '--limit', 1,
                                                    '--page', 1,
                                                    '--datetime','2016-05-03/2019-01-01',
                                                    '--bbox','-180,-90,180,90'])
            assert result.exit_code == 0
            assert 'feature1' in result.output

    def test_search(self, stac_objects, requests_mock, runner):
        for k in stac_objects:
            requests_mock.get(re.compile(url + "/stac" if k != '0.9.0' else url +'/'),
                              json=stac_objects[k]['catalog.json'],
                              status_code=200,
                              headers={'content-type':'application/json'})

            requests_mock.get(re.compile(url+'/collections'), json=stac_objects[k]['collection.json'],
                              status_code=200,
                              headers={'content-type':'application/json'})

            requests_mock.post(re.compile(url + "/stac/search" if k != '0.9.0' else url + '/search'),
                               json=stac_objects[k]['items.json'],
                               status_code=200,
                               headers={'content-type':'application/json'})

            intersects = json.dumps(stac_objects[k]['items.json']['features'][0]['geometry'])

            result = runner.invoke(stac.cli.search, ['--url', url + "/stac" if k != '0.9.0' else url,
                                                    '--collections', 'my_collection1',
                                                    '--ids', 'feature1',
                                                    '--intersects', intersects,
                                                    '--limit', 1,
                                                    '--next', 'aaa',
                                                    '--page', 1,
                                                    '--datetime','2016-05-03/2019-01-01',
                                                    '--bbox','-180,-90,180,90'
                                                    ])

            assert result.exit_code == 0
            assert 'feature1' in result.output


if __name__ == '__main__':
    pytest.main(['--color=auto', '--no-cov'])
