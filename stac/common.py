#
# This file is part of Python Client Library for STAC.
# Copyright (C) 2019-2021 INPE.
#
# Python Client Library for STAC is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Common objects for STAC."""

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
