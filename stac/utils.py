#
# This file is part of Python Client Library for STAC.
# Copyright (C) 2019 INPE.
#
# Python Client Library for STAC is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Utility data structures and algorithms."""

import json
import pkg_resources
from jsonschema import validate, RefResolver
import requests
import os

resource_package = __name__

try:

    schema_path = 'file:///{0}/'.format(
        os.path.dirname(pkg_resources.resource_filename('stac.utils', 'jsonschemas/0.8.0/catalog.json')))

    catalog_schema = json.loads(pkg_resources.resource_string(resource_package,
                                                              f'jsonschemas/0.8.0/catalog.json'))

    collection_schema = json.loads(pkg_resources.resource_string(resource_package,
                                                                 f'jsonschemas/0.8.0/collection.json'))

    item_schema = json.loads(pkg_resources.resource_string(resource_package,
                                                           f'jsonschemas/0.8.0/item.json'))
    item_collection_schema = json.loads(pkg_resources.resource_string(resource_package,
                                                                      f'jsonschemas/0.8.0/itemcollection.json'))
except Exception as e:
    raise Exception(f'Error while loading validation schemas: {e}')

class Utils:
    """Utils STAC object."""

    @staticmethod
    def _get(url, params=None):
        """Query the STAC service using HTTP GET verb and return the result as a JSON document.

        :param url: The URL to query must be a valid STAC endpoint.
        :type url: str

        :param params: (optional) Dictionary, list of tuples or bytes to send
        in the query string for the underlying `Requests`.
        :type params: dict

        :rtype: dict

        :raises ValueError: If the response body does not contain a valid json.
        """
        response = requests.get(url, params=params)

        response.raise_for_status()

        content_type = response.headers.get('content-type')

        if content_type not in ('application/json', 'application/geo+json'):
            raise ValueError('HTTP response is not JSON: Content-Type: {}'.format(content_type))

        return response.json()

class Link(dict):
    """Link object."""

    def __init__(self, data):
        """Initialize instance with dictionary data.

        :param data: Dict with Link metadata.
        """
        super(Link, self).__init__(data or {})

    @property
    def rel(self):
        """:return: the Link relation."""
        return self['rel']

    @property
    def href(self):
        """:return: the Link url."""
        return self['href']

    @property
    def type(self):
        """:return: the type of the Link object."""
        return self['type']

    @property
    def title(self):
        """:return: the title of the Link object."""
        return self['title']


class Extent(dict):
    """The Extent object."""

    def __init__(self, data):
        """Initialize instance with dictionary data.

        :param data: Dict with Extent metadata.
        """
        super(Extent, self).__init__(data or {})

    @property
    def spatial(self):
        """:return: the spatial extent."""
        return self['spatial']

    @property
    def temporal(self):
        """:return: the temporal extent."""
        return self['temporal']


class Provider(dict):
    """The Provider Object."""

    def __init__(self, data):
        """Initialize instance with dictionary data.

        :param data: Dict with Provider metadata.
        """
        super(Provider, self).__init__(data or {})

    @property
    def name(self):
        """:return: the Provider name."""
        return self['name']

    @property
    def description(self):
        """:return: the Provider description."""
        return self['description']

    @property
    def roles(self):
        """:return: the Provider roles."""
        return self['description']

    @property
    def url(self):
        """:return: the Provider url."""
        return self['url']


class Catalog(dict):
    """The STAC Catalog."""

    def __init__(self, data, validation=False):
        """Initialize instance with dictionary data.

        :param data: Dict with catalog metadata.
        :param validation: True if the Catalog must be validated. (Default is False)
        """
        if validation:
            validate(data, schema=catalog_schema)
        super(Catalog, self).__init__(data or {})

    @property
    def stac_version(self):
        """:return: the STAC version."""
        return self['stac_version']

    @property
    def stac_extensions(self):
        """:return: the STAC extensions."""
        return self['stac_extensions']

    @property
    def id(self):
        """:return: the catalog identifier."""
        return self['id']

    @property
    def title(self):
        """:return: the catalog title."""
        return self['title'] if 'title' in self else None

    @property
    def description(self):
        """:return: the catalog description."""
        return self['description']

    @property
    def summaries(self):
        """:return: the catalog summaries."""
        return self['summaries']

    @property
    def links(self):
        """:return: a list of resources in the catalog."""
        return self['links']


class Collection(Catalog):
    """The STAC Collection."""

    def __init__(self, data, validation=False):
        """Initialize instance with dictionary data.

        :param data: Dict with collection metadata.
        :param validation: True if the Collection must be validated. (Default is False)        
        """
        if validation:
            validate(data, schema=collection_schema, resolver=RefResolver(schema_path, collection_schema))
        super(Collection, self).__init__(data or {})

    @property
    def keywords(self):
        """:return: the Collection list of keywords."""
        return self['keywords']

    @property
    def version(self):
        """:return: the Collection version."""
        return self['version']

    @property
    def license(self):
        """:return: the Collection license."""
        return self['license']

    @property
    def providers(self):
        """:return: the Collection list of providers."""
        return self['providers']

    @property
    def extent(self):
        """:return: the Collection extent."""
        return self['extent']

    @property
    def properties(self):
        """:return: the Collection properties."""
        return self['properties']

    def get_items(self, filter=None):
        """:return: the Collection list of items."""
        for link in self['links']:
            if link['rel'] == 'items':
                data = Utils._get(link['href'], params=filter)
                return ItemCollection(data)
        return ItemCollection({})


class Geometry(dict):
    """The Geometry Object."""

    def __init__(self, data):
        """Initialize instance with dictionary data.

        :param data: Dict with Geometry metadata.
        """
        super(Geometry, self).__init__(data or {})

    @property
    def type(self):
        """:return: the Geometry type."""
        return self['type']

    @property
    def coordinates(self):
        """:return: the Geometry coordinates."""
        return self['coordinates']


class Item(dict):
    """The GeoJSON Feature of a STAC Item."""

    def __init__(self, data, validation=False):
        """Initialize instance with dictionary data.

        :param data: Dict with Item metadata.
        :param validation: True if the Item must be validated. (Default is False)
        """
        if validation:
            validate(data, schema=item_schema, )
        super(Item, self).__init__(data or {})

    @property
    def stac_version(self):
        """:return: the STAC version."""
        return self['stac_version']

    @property
    def stac_extensions(self):
        """:return: the STAC extensions."""
        return self['stac_extensions']

    @property
    def id(self):
        """:return: the Item identifier."""
        return self['id']
    
    @property
    def type(self):
        """:return: the Item type."""
        return self['type']

    @property
    def bbox(self):
        """:return: the Item Bounding Box."""
        return self['bbox']

    @property
    def collection(self):
        """:return: the Item Collection."""
        return self['collection']

    @property
    def geometry(self):
        """:return: the Item Geometry."""
        return self['geometry']

    @property
    def properties(self):
        """:return: the Item properties."""
        return self['properties']

    @property
    def links(self):
        """:return: the Item related links."""
        return self['links']

    @property
    def assets(self):
        """:return: the Item related assets."""
        return self['assets']


class ItemCollection(dict):
    """The GeoJSON Feature Collection of STAC Items."""

    def __init__(self, data, validation=False):
        """Initialize instance with dictionary data.

        :param data: Dict with Item Collection metadata.
        :param validation: True if the Item Collection must be validated. (Default is False)        
        """
        if validation:
            validate(data, schema=item_collection_schema, resolver=RefResolver(schema_path, item_collection_schema))
        super(ItemCollection, self).__init__(data or {})

    @property
    def type(self):
        """:return: the Item Collection type."""
        return self['type']

    @property
    def features(self):
        """:return: the Item Collection list of GeoJSON Features."""
        return [Item(i) for i in self['features']]
