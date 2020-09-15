#
# This file is part of Python Client Library for STAC.
# Copyright (C) 2019 INPE.
#
# Python Client Library for STAC is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Utility data structures and algorithms."""
import json

import jinja2
import requests
from jsonschema import RefResolver, validate
from pkg_resources import resource_filename, resource_string

base_schemas_path = resource_filename(__name__, 'jsonschemas/')
templateLoader = jinja2.FileSystemLoader( searchpath=resource_filename(__name__, 'templates/'))
templateEnv = jinja2.Environment( loader=templateLoader )

class Utils:
    """Utils STAC object."""

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
        response = None

        if params is not None:
            if 'intersects' in params or 'query' in params:
                if 'collections' in params and isinstance(params['collections'], str):
                    params['collections'] = params['collections'].split(',')
                if 'ids' in params and isinstance(params['ids'], str):
                    params['ids'] = params['ids'].split(',')
                if 'bbox' in params and isinstance(params['bbox'], str):
                    params['bbox'] = [float(coord) for coord in params['bbox'].split(',')]

                response = requests.post(url, json=params)
            else:
                response = requests.get(url, params=params)
        else:
            response = requests.get(url)

        response.raise_for_status()

        content_type = response.headers.get('content-type')

        if content_type not in ('application/json', 'application/geo+json'):
            raise ValueError('HTTP response is not JSON: Content-Type: {}'.format(content_type))

        return response.json()


    @staticmethod
    def validate(stac_object):
        """Validate a STAC Object using its jsonschema.

        :raise ValidationError: raise a ValidationError if the STAC Object couldn't be validated.
        """
        resolver = RefResolver(f'file://{base_schemas_path}{stac_object.stac_version}/', None)

        validate(stac_object, stac_object._schema, resolver=resolver)

    @staticmethod
    def render_html(template_name, **kwargs):
        """Render Jinja2 HTML template."""
        template = templateEnv.get_template( template_name )
        return template.render(**kwargs)
