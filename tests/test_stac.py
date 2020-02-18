#
# This file is part of Python Client Library for STAC.
# Copyright (C) 2019 INPE.
#
# Python Client Library for STAC is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Unit-test for STAC operations."""


import os
from unittest.mock import Mock, patch

import pytest
import requests

import stac

url =  os.environ.get('STAC_SERVER_URL', 'http://localhost')

class TestUtils:
    @classmethod
    def setup(cls):
        cls.mock_get_patcher = patch('requests.get')
        cls.mock_get = cls.mock_get_patcher.start()
    @classmethod
    def teardown(cls):
        cls.mock_get_patcher.stop()

    def test_ok(self):
        self.mock_get.return_value = Mock(status_code=200, headers={'content-type':'application/json'})
        self.mock_get.return_value.json.return_value = {"key":"value"}
        stac.Utils._get(url)

    def test_error(self):
        self.mock_get.return_value = Mock(status_code=200, headers={'content-type':'text/plain'})
        self.mock_get.return_value.json.return_value = {"key":"value"}
        with pytest.raises(ValueError):
            stac.Utils._get(url)

class TestStac:
    @classmethod
    def setup(cls):
        cls.mock_get_patcher = patch('requests.get')
        cls.mock_get = cls.mock_get_patcher.start()
        cls.mock_get.return_value = Mock(status_code=200, headers={'content-type':'application/json'})

        cls.s = stac.STAC(url)

        cls.conforms = {"conformsTo":
            ["http://www.opengis.net/spec/wfs-1/3.0/req/core",
            "http://www.opengis.net/spec/wfs-1/3.0/req/oas30",
            "http://www.opengis.net/spec/wfs-1/3.0/req/html",
            "http://www.opengis.net/spec/wfs-1/3.0/req/geojson"]
        }

        cls.catalog = {
            'title':'my_catalog title',
            'stac_version':'0.7.0',
            'id':'stac',
            'description':'my_catalog description',
            'links':[
                {
                    'href':f'{url}/collection/my_collection1',
                    'title':'my_collection1',
                    'rel': 'child',
                    'type': 'application/json'
                }
            ]
        }


        cls.collection = {
                "stac_version": "0.7.0",
                "id": "my_collection1",
                "title": "my_collection1",
                "description": "my_collection1",
                "version":"0.1.0",
                "keywords": [
                "landsat"
                ],
                "extent":{
                    "spatial": [
                        -180,
                        -90,
                        180,
                        90
                    ],
                "temporal":
                    [
                        "2013-06-01T00:00:00Z",
                        None
                    ]
                },
                "providers": [
                    {
                        "name":"my_provider",
                        "description": "my_provider_description",
                        "roles": ["producer"],
                        "url": "my_provider_url"
                    }
                ],
                "license": "MIT",
                "properties": {"datetime": "2000-01-01"},
                "links": [
                    {
                        "rel": "self",
                        "href": f"{url}/collections/my_collection1"
                    },
                    {
                        "rel": "items",
                        "href": f"{url}/collections/my_collection1/items"
                    }
                ]
            }

        cls.items = {
            "type":"FeatureCollection",
            "features":[
                    {"type": "Feature",
                     "stac_version": "0.7.0",
                    "id": "feature1",
                    "description": "aaa",
                    "bbox": [-122.59750209, 37.48803556, -122.2880486, 37.613537207],
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [
                        [[-122.308150179, 37.488035566],
                            [-122.597502109, 37.538869539],
                            [-122.576687533, 37.613537207],
                            [-122.288048600, 37.562818007],
                            [-122.308150179, 37.488035566]]]
                    },
                    "properties": {
                        "datetime": "2016-05-03T13:21:30.040Z"
                    },
                    "collection": "my_collection1",
                    "links": [
                        {
                        "rel": "self",
                        "href":  f"{url}/collections/my_collection1/feature1"
                        },
                        {
                        "rel": "collection",
                        "href": f"{url}/collections/my_collection1"
                        }
                    ],
                    "assets": {
                        "thumbnail": {
                        "href": f"{url}/collections/my_collection1/feature1/thumbnail.png",
                        "title": "Thumbnail",
                        "type": "image/jpeg"
                        }
                    }
                },
                {"type": "Feature",
                    "id": "feature2",
                    "stac_version": "0.7.0",
                    "bbox": [-122.59750209, 37.48803556, -122.2880486, 37.613537207],
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [
                        [
                            [-122.308150179, 37.488035566],
                            [-122.597502109, 37.538869539],
                            [-122.576687533, 37.613537207],
                            [-122.288048600, 37.562818007],
                            [-122.308150179, 37.488035566]
                        ]
                        ]
                    },
                    "properties": {
                        "datetime": "2016-05-10T13:21:30.040Z"
                    },
                    "collection": "my_collection1",
                    "links": [
                        {
                        "rel": "self",
                        "href": f"{url}/collections/my_collection1/feature2"
                        },
                        {
                        "rel": "collection",
                        "href": f"{url}/collections/my_collection1"
                        }
                    ],
                    "assets": {
                        "thumbnail": {
                        "href": f"{url}/collections/my_collection1/feature1/thumbnail.png",
                        "title": "Thumbnail",
                        "type": "image/jpeg"
                        }
                    }
                }
            ]
        }

    @classmethod
    def teardown(cls):
        cls.mock_get_patcher.stop()

    def test_stac(self):
        assert self.s.url == url
        assert repr(self.s) == f'stac("{url}")'
        assert str(self.s) == f'<STAC [{url}]>'


    def test_conformance(self):
        self.mock_get.return_value = Mock(status_code=200, headers={'content-type':'application/json'})
        self.mock_get.return_value.json.return_value = self.conforms
        response = self.s.conformance
        assert response == self.conforms

    def test_catalog(self):
        self.mock_get.return_value = Mock(status_code=200, headers={'content-type':'application/json'})
        self.mock_get.return_value.json.return_value = self.catalog
        response = self.s.catalog
        assert self.s._catalog.stac_version
        assert self.s._catalog.id
        assert self.s._catalog.description
        assert self.s._catalog.title
        assert self.s._catalog.links[0].type
        assert self.s._catalog.links[0].title
        assert self.s._catalog.links[0].href
        assert self.s._catalog.links[0].rel
        assert response == set(['my_collection1'])

    def test_collection(self):
        self.mock_get.return_value = Mock(status_code=200, headers={'content-type':'application/json'})
        self.mock_get.return_value.json.return_value = self.catalog
        response = self.s.catalog

        self.mock_get.return_value = Mock(status_code=200, headers={'content-type':'application/json'})
        self.mock_get.return_value.json.return_value = self.collection
        collection = self.s.collection('my_collection1')

        assert collection == self.collection
        assert collection.keywords
        assert collection.version
        assert collection.license
        assert collection.properties
        assert collection.extent.spatial
        assert collection.extent.temporal
        assert collection.providers[0].name
        assert collection.providers[0].description
        assert collection.providers[0].roles
        assert collection.providers[0].url

    def test_collection_missing(self):
        self.mock_get.return_value = Mock(status_code=200, headers={'content-type':'application/json'})
        self.mock_get.return_value.json.return_value = self.catalog
        response = self.s.catalog

        self.mock_get.return_value = Mock(status_code=500, headers={'content-type':'application/json'})
        self.mock_get.side_effect = requests.exceptions.HTTPError
        self.mock_get.return_value.json.return_value = {}

        with pytest.raises(KeyError):
            self.s.collection('missing_collection')

    def test_collection_without_catalog(self):
        self.mock_get.return_value = Mock(status_code=200, headers={'content-type':'application/json'})
        self.mock_get.return_value.json.return_value = self.collection
        response = self.s.collections

        assert self.s.collection('my_collection1') == self.collection

    def test_item(self):
        self.mock_get.return_value = Mock(status_code=200, headers={'content-type':'application/json'})
        self.mock_get.return_value.json.return_value = self.catalog
        response = self.s.catalog

        self.mock_get.return_value = Mock(status_code=200, headers={'content-type':'application/json'})
        self.mock_get.return_value.json.return_value = self.collection
        response = self.s.collections

        self.mock_get.return_value = Mock(status_code=200, headers={'content-type':'application/json'})
        self.mock_get.return_value.json.return_value = self.items

        response = self.s.collection('my_collection1').get_items()
        assert response.type
        item = response.features[0]
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

    def test_item_id(self):
        self.mock_get.return_value.json.return_value = self.catalog
        response = self.s.catalog

        self.mock_get.return_value = Mock(status_code=200, headers={'content-type':'application/json'})
        self.mock_get.return_value.json.return_value = self.collection
        response = self.s.collections

        self.mock_get.return_value = Mock(status_code=200, headers={'content-type':'application/json'})
        self.mock_get.return_value.json.return_value = self.items['features'][0]

        response = self.s.collection('my_collection1').get_items(item_id='feature1')
        assert response.id == 'feature1'

    def test_item_empty(self):
        self.mock_get.return_value = Mock(status_code=200, headers={'content-type':'application/json'})
        self.mock_get.return_value.json.return_value = self.collection
        collection = self.s.collection('my_collection1')

        self.mock_get.return_value = Mock(status_code=200, headers={'content-type':'application/json'})
        self.mock_get.return_value.json.return_value = self.items['features'][0]
        collection['links'].pop(1)
        assert collection.get_items() == stac.ItemCollection({})

    def test_search(self):
        self.mock_get.return_value.json.return_value = self.catalog
        response = self.s.catalog

        self.mock_get.return_value = Mock(status_code=200, headers={'content-type':'application/json'})
        self.mock_get.return_value.json.return_value = self.items

        response = self.s.search()

        assert response.features[0].id == 'feature1'

if __name__ == '__main__':
    pytest.main(['--color=auto', '--no-cov'])
