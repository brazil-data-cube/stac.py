#
# This file is part of Python Client Library for STAC.
# Copyright (C) 2019-2021 INPE.
#
# Python Client Library for STAC is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""STAC Item module."""

import json
import os
import shutil
from collections.abc import Iterable
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

    def download(self, dir=None): # pragma: no cover
        """Download the asset to an indicated folder.

        If tqdm is installed a progressbar will be shown.

        :param dir: Directory path to download the asset, if left None,
                    the asset will be downloaded to the current
                    working directory.
        :return: path to downloaded file.
        """
        filename = urlparse(self['href'])[2].split('/')[-1]

        if dir:
            filename = os.path.join(dir, filename)
            os.makedirs(os.path.dirname(filename), exist_ok=True)

        response = requests.get(self['href'], stream=True)

        response.raise_for_status()

        try:
            from tqdm import tqdm

            with tqdm.wrapattr(open(filename, 'wb'), 'write', miniters=1,
                        total=int(response.headers.get('content-length', 0)),
                        desc=filename) as fout:
                for chunk in response.iter_content(chunk_size=4096):
                    fout.write(chunk)

        except ImportError:
            with open(filename, 'wb') as f:
                shutil.copyfileobj(response.raw, f)

        return filename


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
        self._providers = [Provider(p) for p in self['providers']] if 'providers' in self else []

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
        return self._providers

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

        self._schema = json.loads(resource_string(__name__, f'jsonschemas/{self.stac_version}/item.json'))

        if self._validate:
            Utils.validate(self)

        self._assets = {key: Asset(value) for key,value in self['assets'].items()} if 'assets' in self else {}
        self._links = [Link(link) for link in self['links']] if 'links' in self else []

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
        return self._links

    @property
    def assets(self):
        """:return: the Item related assets."""
        return self._assets

    @property
    def schema(self):
        """:return: the Collection jsonschema."""
        return self._schema

    def _repr_html_(self): # pragma: no cover
        """HTML repr."""
        return Utils.render_html('item.html', item=self)

    def download(self, dir=None): # pragma: no cover
        """Download an asset given a band name.

        :param dir: Directory path to download the asset, if left None,
                    the asset will be downloaded to the current
                    working directory.
        :return: path to downloaded file.
        """
        output = dict()
        for asset_name, asset in self.assets.items():
            output[asset_name] = asset.download(dir=dir)

        return output

    def read(self, band_name, window=None, bbox=None, crs=None): # pragma: no cover
        """Read an asset given a band name.

        Notes:
            You must install the extra `geo` containing the `rasterio` and `Shapely` library
            in order to use this method:

                pip install stac.py[geo]

        :param band_name: Band name used in the asset
        :type band_name: str
        :param window: window crop
        :type window: raster.windows.Window
        :param bbox: The bounding box
        :type bbox: Union[str,Tuple[float],List[float],BaseGeometry]
        :param crs: The Coordinate Reference System
        :return: the asset as a numpy array
        :rtype: numpy.ndarray
        """
        import rasterio
        from rasterio.crs import CRS
        from rasterio.warp import transform
        from rasterio.windows import from_bounds

        with rasterio.open(self.assets[band_name]['href']) as dataset:
            if bbox:
                bbox = Utils.build_bbox(bbox)

                w, s, e, n = bbox.bounds

                source_crs = CRS.from_string('EPSG:4326')

                if crs:
                    source_crs = CRS.from_string(crs)

                t = transform(source_crs, dataset.crs, [w, e], [s, n])
                window = from_bounds(t[0][0], t[1][0], t[0][1], t[1][1], dataset.transform)

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

        self._features = [Item(i, self._validate) for i in self['features']] if 'features' in self else []
        self._links = [Link(i) for i in self['links']] if 'links' in self else []

    @property
    def type(self):
        """:return: the Item Collection type."""
        return self['type']

    @property
    def features(self):
        """:return: the Item Collection list of GeoJSON Features."""
        return self._features

    @property
    def links(self):
        """:return: the Item Collection list of GeoJSON Features."""
        return self._links

    def _repr_html_(self): # pragma: no cover
        """HTML repr."""
        return Utils.render_html('itemcollection.html', itemcollection=self)

    def __iter__(self): # pragma: no cover
        """Feature iterator."""
        return self.features.__iter__()

    def __next__(self): # pragma: no cover
        """Next Feature iterator."""
        return next(self.features)
