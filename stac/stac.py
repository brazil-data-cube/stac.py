#
# This file is part of Python Client Library for STAC.
# Copyright (C) 2019 INPE.
#
# Python Client Library for STAC is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Python API client wrapper for STAC."""

import requests

from .utils import Catalog, Collection, Item, ItemCollection


class Stac:
    """This class implements a Python API client wrapper for STAC.

    See https://github.com/radiantearth/stac-spec for more information on STAC.

    :param url: The STACrver URL.
    :type url: str
    """

    def __init__(self, url):
        """Create a STAC client attached to the given host address (an URL)."""
        self._url = url if url[-1] != '/' else url[0:-1]

    def capabilities(self):
        """Return the list of available routes for the STAC API."""
        return self._get('{}'.format(self._url))

    def conformance(self):
        """Return the list of conformance classes that the server conforms to."""
        return self._get('{}/conformance'.format(self._url))

    def catalog(self):
        """Return the root catalog or collection."""
        url = '{}/stac'.format(self._url)
        data = self._get(url)
        return Catalog(data)

    def collections(self):
        """Return the root catalog or collection."""
        url = '{}/collections'.format(self._url)
        data = self._get(url)
        return Catalog(data)

    def collection(self, collection_id):
        """Return the given collection.
        :param collection_id: A str for a given collection_id.
        :type collection_id: str

        :returns: A STAC Collection.
        :rtype: dict
        """
        url = '{}/collections/{}'.format(self._url, collection_id)
        data = self._get(url)
        return Collection(data)

    def collection_items(self, collection_id, filter=None):
        """Return the items of a given collection.
        :param collection_id: A str for a given collection_id.
        :type collection_id: str

        :returns: A GeoJSON FeatureCollection with items of a given collection.
        :rtype: dict
        """
        url = '{}/collections/{}/items'.format(self._url, collection_id)
        data = self._get(url, params=filter)
        return ItemCollection(data)

    def collection_item(self, collection_id, item_id):
        """Return a given item of a given collection.
        :param collection_id: A str for a given collection_id.
        :type collection_id: str

        :param item_id: A str for a given item_id.
        :type item_id: str

        :returns: A GeoJSON Feature of the item from a given collection.
        :rtype: dict
        """
        url = '{}/collections/{}/items/item_id'.format(self._url, collection_id, item_id)
        data = self._get(url)
        return Item(data)

    def search(self, filter=None):
        """Retrieve Items matching a filter.

        :param filter: (optional) A dictionary with valid STAC query parameters.
        :type filter: dict

        :returns: A feature collection.
        :rtype: dict
        """
        url = '{}/stac/search'.format(self._url)
        data = self._get(url, params=filter)
        return ItemCollection(data)

    @property
    def url(self):
        """Return the STAC server instance URL."""
        return self._url

    def __repr__(self):
        """Return the string representation of a STAC object."""
        text = 'stac("{}")'.format(self.url)
        return text

    def __str__(self):
        """Return the string representation of a STAC object."""
        return '<STAC [{}]>'.format(self.url)

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
