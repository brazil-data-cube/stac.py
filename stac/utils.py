#
# This file is part of Python Client Library for STAC.
# Copyright (C) 2019-2021 INPE.
#
# Python Client Library for STAC is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Utility data structures and algorithms."""

from collections.abc import Iterable

import jinja2
import requests
from jsonschema import RefResolver, validate
from pkg_resources import resource_filename

base_schemas_path = resource_filename(__name__, 'jsonschemas/')
templateLoader = jinja2.FileSystemLoader( searchpath=resource_filename(__name__, 'templates/'))
templateEnv = jinja2.Environment( loader=templateLoader )


class Utils:
    """Utils STAC object."""

    @staticmethod
    def _get(url, params=None, **request_kwargs):
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

                response = requests.post(url, json=params, **request_kwargs)
            else:
                if 'collections' in params and type(params['collections']) in (tuple, list):
                    params['collections'] = ','.join(params['collections'])
                response = requests.get(url, params=params,  **request_kwargs)
        else:
            response = requests.get(url,  **request_kwargs)

        response.raise_for_status()

        content_type = response.headers.get('content-type')

        if content_type not in ('application/json', 'application/geo+json'):
            raise ValueError('HTTP response is not JSON: Content-Type: {}'.format(content_type))

        return response.json()

    @staticmethod
    def validate(stac_object):
        """Validate a STAC Object using its jsonschema.

        :param stac_object: A STAC object.

        :raise ValidationError: raise a ValidationError if the STAC Object couldn't be validated.
        """
        resolver = RefResolver(f'file://{base_schemas_path}{stac_object.stac_version}/', None)

        validate(stac_object, stac_object.schema, resolver=resolver)

    @staticmethod
    def render_html(template_name, **kwargs): # pragma: no cover
        """Render Jinja2 HTML template."""
        template = templateEnv.get_template( template_name )
        return template.render(**kwargs)

    @staticmethod
    def build_bbox(bbox):
        """Define a common way to create the minimum bounding region.

        :param bbox: The bounding box
        :type bbox: Union[str,List[float],Tuple[float]]

        :rtype: shapely.geometry.base.BaseGeometry
        """
        from shapely.geometry import box
        from shapely.geometry.base import BaseGeometry

        if isinstance(bbox, str):
            try:
                bbox = [float(elm.strip()) for elm in bbox.split(',')]
            except ValueError:
                raise TypeError(f'Invalid bbox {bbox}')

        if isinstance(bbox, Iterable):
            bbox = box(*bbox)

        if not isinstance(bbox, BaseGeometry) or bbox.is_empty:
            raise TypeError(f'Invalid bbox {bbox}')

        return bbox

    @staticmethod
    def build_bbox_as_str(bbox) -> str:
        """Retrieve the string representation of a minimum bounding region.

        :param bbox: The bounding box

        :rtype: str
        """
        bounds = Utils.build_bbox(bbox).bounds

        return f'{bounds[0]},{bounds[1]},{bounds[2]},{bounds[3]}'

    @staticmethod
    def safe_request(url: str, method: str = 'get', **kwargs) -> requests.Response:
        """Query the given URL for any HTTP Request and handle minimal HTTP Exceptions.

        :param url: The URL to query.
        :param method: HTTP Method name.
        :param kwargs: (optional) Any argument supported by `requests.request <https://docs.python-requests.org/en/latest/api/#requests.request>`_

        :raise HTTPError - For any HTTP error related.
        :raise ConnectionError - For any error related ConnectionError such InternetError

        :rtype: requests.Response
        """
        try:
            response = requests.request(method, url, **kwargs)

            response.raise_for_status()

            return response
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(f'(Connection Refused) {e.request.url}')
        except requests.exceptions.HTTPError as e:
            if e.response is None:
                raise

            reason = e.response.reason
            msg = str(e)
            if e.response.status_code == 403:
                if e.request.headers.get('x-api-key') or 'access_token=' in e.request.url:
                    msg = "You don't have permission to request this resource."
                else:
                    msg = 'Missing Authentication Token.'  # TODO: Improve this message for any STAC provider.
            elif e.response.status_code == 500:
                msg = 'Could not request this resource.'

            raise requests.exceptions.HTTPError(f'({reason}) {msg}', request=e.request, response=e.response)
