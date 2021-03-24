#
# This file is part of Python Client Library for STAC.
# Copyright (C) 2019-2021 INPE.
#
# Python Client Library for STAC is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Python API client wrapper for STAC."""
import warnings

from requests import HTTPError

from .catalog import Catalog
from .collection import Collection
from .item import ItemCollection
from .utils import Utils


class STAC:
    """This class implements a Python API client wrapper for STAC.

    See https://github.com/radiantearth/stac-spec for more information on STAC.

    :param url: URL for the Root STAC Catalog.
    :type url: str
    """

    def __init__(self, url, validate=False, access_token=None):
        """Create a STAC client attached to the given host address (an URL).

        :param url: URL for the Root STAC Catalog.
        :type url: str
        :param validate: True if responses should ve validated
        :type validate: bool
        :param access_token: Authentication for the STAC API
        :type access_token: str
        """
        self._url = url
        self._collections = dict()
        self._catalog = dict()
        self._validate = validate
        self._access_token = f'?access_token={access_token}' if access_token else ''

    @property
    def conformance(self): # pragma: no cover
        """Return the list of conformance classes that the server conforms to."""
        return Utils._get('{}/conformance'.format(self._url))

    @property
    def catalog(self):
        """
        Retrieve the available collections in the STAC Catalog.

        :return list of available collections.
        """
        if len(self._collections) > 0:
            return list(self._collections.keys())

        url = f'{self._url}{self._access_token}'
        response = Utils._get(url)

        self._catalog = Catalog(response, self._validate)

        for i in self._catalog.links:
            if i.rel == 'child':
                if '?' in i.href:  # pragma: no cover
                    collection_name = i.href.split('/')[-1]
                    self._collections[collection_name[:collection_name.index('?')]] = None
                else:
                    self._collections[i.href.split('/')[-1]] = None
        return list(self._collections.keys())


    @property
    def collections(self):
        """Return all available collections.

        :returns: A dict containing all collections.
        :rype: dict
        """
        url = '/'.join(self._url.split('/')[:-1]) if self._url.endswith('/stac') else self._url
        data = Utils._get(f'{url}/collections{self._access_token}')
        self._collections = {collection['id']: Collection(collection, self._validate) for collection in data['collections']}

        return self._collections


    def collection(self, collection_id):
        """Return the given collection.

        :param collection_id: A str for a given collection_id.
        :type collection_id: str

        :returns: A STAC Collection.
        :rtype: dict
        """
        if collection_id in self._collections.keys() and \
            self._collections[collection_id] is not None:
            return self._collections[collection_id]
        try:
            url = '/'.join(self._url.split('/')[:-1]) if self._url.endswith('/stac') else self._url
            data = Utils._get(f'{url}/collections/{collection_id}{self._access_token}')
            self._collections[collection_id] = Collection(data, self._validate)
        except HTTPError as e:
            raise KeyError(f'Could not retrieve information for collection: {collection_id}')
        return self._collections[collection_id]


    def search(self, filter=None):
        """Retrieve Items matching a filter.

        :param filter: (optional) A dictionary with valid STAC query parameters.
        :type filter: dict

        :returns: A GeoJSON FeatureCollection.
        :rtype: dict
        """
        if not self._catalog:  # pragma: no cover
            self.catalog

        url = f'{self._url}/search{self._access_token}'

        if filter is not None and 'bbox' in filter:
            filter['bbox'] = Utils.build_bbox_as_str(filter['bbox'])

        data = Utils._get(url, params=filter)
        return ItemCollection(data, self._validate)

    @property
    def url(self):
        """Return the STAC server instance URL."""
        return self._url

    def __repr__(self):
        """Return the string representation of a STAC object."""
        text = 'stac("{}")'.format(self.url)
        return text

    def _repr_html_(self): # pragma: no cover
        """HTML repr."""
        collections = str()
        for collection in self.catalog:
            collections += f"<li>{collection}</li>"
        return f"""<p>STAC</p>
                    <ul>
                     <li><b>URL:</b> {self._url}</li>
                     <li><b>Collections:</b></li>
                     <ul>
                     {collections}
                     </ul>
                   </ul>
               """

    def __str__(self):
        """Return the string representation of a STAC object."""
        return '<STAC [{}]>'.format(self.url)
