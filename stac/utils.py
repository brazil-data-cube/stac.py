#
# This file is part of Python Client Library for STAC.
# Copyright (C) 2019 INPE.
#
# Python Client Library for STAC is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Utility data structures and algorithms."""

class catalog(dict):
    """The root STAC Catalog."""

    def __init__(self, data):
        """Initialize instance with dictionary data.

        :param data: Dict with catalog metadata.
        """
        super(catalog, self).__init__(data or {})


    @property
    def stac_version(self):
        """Return the STAC version."""
        return self['stac_version']


    @property
    def stac_extensions(self):
        """Return the list of supported extensions."""
        return self['stac_extensions'] if 'stac_extensions' in self else None


    @property
    def id(self):
        """Return the catalog identifier."""
        return self['id']


    @property
    def title(self):
        """Return the catalog title."""
        return self['title'] if 'title' in self else None


    @property
    def description(self):
        """Return the catalog description."""
        return self['description']


    @property
    def summaries(self):
        """Return a summary about the catalog."""
        return self['summaries'] if 'summaries' in self else None


    @property
    def links(self):
        """Return a list of resources in the catalog."""
        return self['links']
