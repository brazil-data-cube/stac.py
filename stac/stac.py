#
# This file is part of Python Client Library for STAC.
# Copyright (C) 2019 INPE.
#
# Python Client Library for STAC is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Python API client wrapper for STAC."""

from .catalog import Catalog
from .collection import Collection
from .utils import Utils
from .item import ItemCollection

class STAC:
    """This class implements a Python API client wrapper for STAC.

    See https://github.com/radiantearth/stac-spec for more information on STAC.

    :param url: The STAC server URL.
    :type url: str
    """

    def __init__(self, url):
        """Create a STAC client attached to the given host address (an URL)."""
        self._url = url if url[-1] != '/' else url[0:-1]
        self._collections = None
        self._catalog = 
    
    @property
    def conformance(self):
        """Return the list of conformance classes that the server conforms to."""
        return Utils._get('{}/conformance'.format(self._url))
    
    @property
    def catalog(self):
        """
        Retrieves the available collections in the STAC Catalog.
        :return list of available collections.
        """
        if self._collections is not None:
            return self._collections.keys()

        self._collections = dict()

        url = '{}/stac'.format(self._url)
        self._catalog = Catalog(Utils._get(url))
        
        for i in self._catalog.links:
            if i.rel == 'child':
                self._collections[i.href.split('/')[-1]] = None
        return self._collections.keys()
    
    @property
    def collections(self):
        """
        :return a dict with the STAC Colletion for every available collection.
        """
        if self._collections is None:
            self.catalog

        for collection_id in self._collections.keys():
            try:
                data = Utils._get(f'{self._url}/collections/{collection_id}')
                self._collections[collection_id] = Collection(data)
            except:
                pass

        return self._collections
    
    def collection(self, collection_id):
        """Return the given collection.
        
        :param collection_id: A str for a given collection_id.
        :type collection_id: str

        :returns: A STAC Collection.
        :rtype: dict
        """
        if collection_id in self._collections.keys() and \
            self._collections[collection_id].value() is not None:
            return self._collections[collection_id] 
        try:
            data = Utils._get(f'{self._url}/collections/{collection_id}')
            self._collections[collection_id] = Collection(data)
        except Exception as e:
            raise Exception(f'Could not retrieve information for collection: {collection_id}')
        return self._collections[collection_id] 


    def search(self, filter=None):
        """Retrieve Items matching a filter.

        :param filter: (optional) A dictionary with valid STAC query parameters.
        :type filter: dict

        :returns: A GeoJSON FeatureCollection.
        :rtype: dict
        """
        url = '{}/stac/search'.format(self._url)
        data = Utils._get(url, params=filter)
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