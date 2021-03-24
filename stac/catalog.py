#
# This file is part of Python Client Library for STAC.
# Copyright (C) 2019-2021 INPE.
#
# Python Client Library for STAC is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""STAC Catalog module."""

import json

from pkg_resources import resource_string

from .common import Link
from .utils import Utils


class Catalog(dict):
    """The STAC Catalog."""

    def __init__(self, data, validate=False):
        """Initialize instance with dictionary data.

        :param data: Dict with catalog metadata.
        :param validate: true if the Catalog should be validate using its jsonschema. Default is False.
        """
        self._validate = validate
        super(Catalog, self).__init__(data or {})

        self._schema = json.loads(resource_string(__name__, f'jsonschemas/{self.stac_version}/catalog.json'))

        if self._validate:
            Utils.validate(self)

        self._links = [Link(link) for link in self['links']] if 'links' in self else []

    @property
    def stac_version(self):
        """:return: the STAC version."""
        return self['stac_version']

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
    def links(self):
        """:return: a list of resources in the catalog."""
        return self._links

    @property
    def schema(self):
        """:return: the Catalog jsonschema."""
        return self._schema
