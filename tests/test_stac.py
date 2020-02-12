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
from unittest.mock import Mock, patch

import stac

url =  os.environ.get('STAC_SERVER_URL', 'http://localhost')


class StacTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_get_patcher = patch('requests.get')
        cls.mock_get = cls.mock_get_patcher.start()
        cls.s = stac.STAC(url)

    @classmethod
    def tearDownClass(cls):
        cls.mock_get_patcher.stop()

    def test_stac(self):
        conforms = {"conformsTo":
            ["http://www.opengis.net/spec/wfs-1/3.0/req/core",
            "http://www.opengis.net/spec/wfs-1/3.0/req/oas30",
            "http://www.opengis.net/spec/wfs-1/3.0/req/html",
            "http://www.opengis.net/spec/wfs-1/3.0/req/geojson"]
        }

        self.mock_get.return_value = Mock(status_code=200, headers={'content-type':'application/json'})
        self.mock_get.return_value.json.return_value = conforms
        response = self.s.conformance
        self.assertEqual(response, conforms)

        catalog = {
            'stac_version':'0.7.0',
            'id':'stac',
            'links':[
                {
                    'href':f'{url}/collection/my_collection1',
                    'title':'my_collection1',
                    'rel': 'child'
                }
            ]
        }

        self.mock_get.return_value = Mock(status_code=200, headers={'content-type':'application/json'})
        self.mock_get.return_value.json.return_value = catalog
        response = self.s.catalog
        self.assertEqual(response, set(['my_collection1']))

        collections = {
                "stac_version": "0.7.0",
                "id": "my_collection1",
                "title": "my_collection1",
                "description": "my_collection1",
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
                "providers": [],
                "license": "MIT",
                "properties": {},
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

        self.mock_get.return_value = Mock(status_code=200, headers={'content-type':'application/json'})
        self.mock_get.return_value.json.return_value = collections
        response = self.s.collections
        self.assertEqual(response['my_collection1'].title, "my_collection1")

        collection = stac.Collection({
                "stac_version": "0.7.0",
                "id": "my_collection1",
                "title": "my_collection1",
                "description": "my_collection1",
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
                "providers": [],
                "license": "MIT",
                "properties": {},
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
            })
        self.assertEqual(self.s.collection('my_collection1'), collection)

        items = {
            "type":"FeatureCollection",
            "features":[
                    {"type": "Feature",
                    "id": "feature1",
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
                        "title": "Thumbnail"
                        }
                    }
                },
                {"type": "Feature",
                    "id": "feature2",
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
                        "title": "Thumbnail"
                        }
                    }
                }
            ]
        }

        self.mock_get.return_value = Mock(status_code=200, headers={'content-type':'application/json'})
        self.mock_get.return_value.json.return_value = items

        response = self.s.collection('my_collection1').get_items()

        self.assertEqual(response.features[0].id, 'feature1')



if __name__ == '__main__':
    unittest.main(verbosity=2)
