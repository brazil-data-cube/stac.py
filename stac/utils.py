#
# This file is part of Python Client Library for STAC.
# Copyright (C) 2019 INPE.
#
# Python Client Library for STAC is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Utility data structures and algorithms."""


class Link(dict):
    """"Link object"""

    def __init__(self, rel, href, type=None, title=None):
        self['rel'] = rel
        self['href'] = href
        if type is not None: self['type'] = type
        if title is not None: self['title'] = title
        super(Link, self)

    @property
    def rel(self):
        """Return the relation of the Link object."""
        return self['rel']

    @property
    def href(self):
        """Return the URL of the Link object."""
        return self['href']

    @property
    def type(self):
        """Return the type of the Link object."""
        return self['type']

    @property
    def title(self):
        """Return the title of the Link object."""
        return self['title']


class Catalog(dict):
    """The root STAC Catalog."""

    def __init__(self, stac_version, id, description, links, **kwargs):
        """Initialize instance with dictionary data.

        :param data: Dict with catalog metadata.
        """
        self['stac_version'] = stac_version
        self['id'] = id
        self['description'] = description
        if isinstance(links, list):
            for link in links:
                if not isinstance(link, Link):
                    raise ValueError("links is not a list of Link objects.")
            self['links'] = links

        super(Catalog, self).__init__(self, **kwargs)

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
