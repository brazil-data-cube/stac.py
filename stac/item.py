#
# This file is part of Python Client Library for STAC.
# Copyright (C) 2019 INPE.
#
# Python Client Library for STAC is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""STAC Item module."""

import json
import shutil
from urllib.parse import urlparse

import requests
from pkg_resources import resource_string

from .common import Link, Provider
from .utils import Utils


class Asset(dict):
    """Asset object."""

    def __init__(self, data):
        """Initialize instance with dictionary data.

        :param data: Dict with Asset metadata.
        """
        super(Asset, self).__init__(data or {})

    @property
    def href(self):
        """:return: the Asset href."""
        return self['href']

    @property
    def title(self):
        """:return: the Asset title."""
        return self['title']

    @property
    def type(self):
        """:return: the Asset type."""
        return self['type']

    def download(self, folder_path=None): # pragma: no cover
        """
        Download the asset to an indicated folder.

        :param folder_path: Folder path to download the asset, if left None,
                            the asset will be downloaded to the current
                            working directory.
        :return: path to downloaded file.
        """
        local_filename = urlparse(self['href'])[2].split('/')[-1]
        if folder_path is not None:
            folder_path += local_filename

        with requests.get(self['href'], stream=True) as r:
            with open(local_filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

        return local_filename


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

class Properties(dict):
    """The Properties Object."""

    def __init__(self, data):
        """Initialize instance with dictionary data.

        :param data: Dict with Properties metadata.
        """
        super(Properties, self).__init__(data or {})

    @property
    def datetime(self):
        """:return: the datetime property."""
        return self['datetime']

    @property
    def license(self):
        """:return: the license property."""
        return self['license']

    @property
    def providers(self):
        """:return: the providers property."""
        return [Provider(p) for p in self['providers']]

    @property
    def title(self):
        """:return: the title property."""
        return self['title']

    @property
    def created(self):
        """:return: the created property."""
        return self['created']

    @property
    def updated(self):
        """:return: the updated property."""
        return self['updated']

class Item(dict):
    """The GeoJSON Feature of a STAC Item."""

    def __init__(self, data, validate=False):
        """Initialize instance with dictionary data.

        :param data: Dict with Item metadata.
        :param validate: true if the Item should be validate using its jsonschema. Default is False.
        """
        self._validate = validate
        super(Item, self).__init__(data or {})
        if self._validate:
            Utils.validate(self)

    @property
    def stac_version(self):
        """:return: the STAC version."""
        return self['stac_version'] if 'stac_version' in self else '0.7.0'

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
        return Geometry(self['geometry'])

    @property
    def properties(self):
        """:return: the Item properties."""
        return Properties(self['properties'])

    @property
    def links(self):
        """:return: the Item related links."""
        return [Link(link) for link in self['links']]

    @property
    def assets(self):
        """:return: the Item related assets."""
        return {key: Asset(value) for key,value in self['assets'].items()}

    @property
    def _schema(self):
        """:return: the Collection jsonschema."""
        schema = resource_string(__name__, f'jsonschemas/{self.stac_version}/item.json')
        _schema = json.loads(schema)
        return _schema

    def _repr_html_(self):
        """HTML repr."""
        return Utils.render_html('item.html', item=self)

    def read(self, band_name, window=None):
        """Read an asset given a band name.

        :param band_name: Band name used in the asset
        :type band_name: str
        :param window: window crop
        :type window: raster.windows.Window
        :return: the asset as a numpy array
        :rtype: numpy.ndarray
        """
        import rasterio

        with rasterio.open(self.assets[band_name]['href']) as dataset:
            asset = dataset.read(1, window=window)

        return asset

class ItemCollection(dict):
    """The GeoJSON Feature Collection of STAC Items."""

    def __init__(self, data, validate=False):
        """Initialize instance with dictionary data.

        :param data: Dict with Item Collection metadata.
        :param validate: true if the Item Collection should be validate using its jsonschema. Default is False.
        """
        self._validate = validate
        super(ItemCollection, self).__init__(data or {})

    @property
    def type(self):
        """:return: the Item Collection type."""
        return self['type']

    @property
    def features(self):
        """:return: the Item Collection list of GeoJSON Features."""
        return [Item(i, self._validate) for i in self['features']]

    @property
    def links(self):
        """:return: the Item Collection list of GeoJSON Features."""
        return [Link(i) for i in self['links']]

    def _repr_html_(self):
        """HTML repr."""
        return Utils.render_html('itemcollection.html', itemcollection=self)

    def __iter__(self):
        """Feature iterator."""
        return self.features.__iter__()

    def __next__(self):
        """Next Feature iterator."""
        return next(self.features)
