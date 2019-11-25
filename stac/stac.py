#
# This file is part of Python Client Library for STAC.
# Copyright (C) 2019 INPE.
#
# Python Client Library for STAC is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Python API client wrapper for STAC."""

import requests
from requests.compat import urljoin


class stac:
    """This class implements a Python API client wrapper for STAC.

    See https://github.com/radiantearth/stac-spec for more information on STAC.

    :param url: The WLTS server URL.
    :type url: str
    """

    def __init__(self, url):
        """Create a STAC client attached to the given host address (an URL)."""
        self._url = url


    def capabilities(self):
        """TODO."""
        pass


    def conformance(self):
        """Return the list of conformance classes that the server conforms to."""
        return self._get('conformance')


    def catalog(self):
        """Return the root catalog or collection."""
        return self._get('stac')


    def collections(self):
        """TODO."""
        pass


    def search(self):
        """TODO."""
        pass


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



    def _get(self, rel_url=None, params=None):
        """Query the STAC service using HTTP GET verb and return the result.

        :rtype: dict

        :raises ValueError: If the response body does not contain a valid json.
        """
        url = urljoin(self._url, rel_url) if rel_url is not None else self._url

        response = requests.get(url)

        response.raise_for_status()

        content_type = response.headers.get('content-type')

        if content_type.count('application/json') == 0:
            raise ValueError('HTTP response is not JSON: Content-Type: {}'.format(content_type))

        return response.json()
