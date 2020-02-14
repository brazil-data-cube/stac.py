#
# This file is part of Python Client Library for STAC.
# Copyright (C) 2019 INPE.
#
# Python Client Library for STAC is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""STAC Collection module."""

from .catalog import Catalog
from .item import Item, ItemCollection
from .utils import Utils


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
        return self['roles']

    @property
    def url(self):
        """:return: the Provider url."""
        return self['url']


class Collection(Catalog):
    """The STAC Collection."""

    def __init__(self, data):
        """Initialize instance with dictionary data.

        :param data: Dict with collection metadata.
        """
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
        return [Provider(provider) for provider in self['providers']]

    @property
    def extent(self):
        """:return: the Collection extent."""
        return Extent(self['extent'])

    @property
    def properties(self):
        """:return: the Collection properties."""
        return self['properties']

    def get_items(self, item_id=None, filter=None):
        """:return: A GeoJSON FeatureCollection of STAC Items from the collection."""
        for link in self['links']:
            if link['rel'] == 'items':
                if item_id is not None:
                    data = Utils._get(f'{link["href"]}/{item_id}')
                    return Item(data)
                data = Utils._get(link['href'], params=filter)
                return ItemCollection(data)
        return ItemCollection({})
