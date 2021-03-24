#
# This file is part of Python Client Library for STAC.
# Copyright (C) 2019-2021 INPE.
#
# Python Client Library for STAC is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Command line interface for the STAC client."""
import json

import click

from .stac import STAC


@click.group()
def cli():
    """STAC on command line."""
    pass #pragma: no cover

@click.command()
@click.option('--url', default=None, help='The STAC server address (an URL).')
@click.option('--access-token', default=None, help='Personal Access Token of the BDC Auth')
def catalog(url, access_token=None):
    """Return the list of available collections in the catalog."""
    service = STAC(url, access_token=access_token)

    retval = service.catalog
    for c in retval:
        print(c)


@click.command()
@click.option('--url', default=None, help='The STAC server address (an URL).')
@click.option('--collection-id', default=None, help='The Collection id.')
@click.option('--access-token', default=None, help='Personal Access Token of the BDC Auth')
def collection(url, collection_id, access_token=None):
    """Return the metadata for a given collection."""
    service = STAC(url, access_token=access_token)

    retval = service.collection(collection_id)

    print(json.dumps(retval, indent=2))

@click.command()
@click.option('--url', default=None, help='The STAC server address (an URL).')
@click.option('--collection-id', default=None, help='The collection ID.')
@click.option('--limit', default=10, help='The maximum number of results to return (page size). Defaults to 10')
@click.option('--page', default=1, help='The page number of results. Defaults to 1. (STAC 0.7.0 only)')
@click.option('--datetime', help='Single date, date+time, or a range (\'/\' seperator), formatted to RFC 3339, section 5.6')
@click.option('--bbox', default=None, help='Requested bounding box west, south, east, north')
@click.option('--access-token', default=None, help='Personal Access Token of the BDC Auth')
def items(url, collection_id, limit, page, datetime, bbox, access_token=None):
    """Return items from a given collection ID and filters."""
    service = STAC(url, access_token=access_token)
    service.catalog
    filter = {
        'limit': limit,
        'page': page
    }

    if bbox is not None:
        filter['bbox'] = bbox
    if datetime is not None:
        if service._catalog.stac_version in ['0.8.0', '0.8.1']:
            filter['datetime'] = datetime
        elif service._catalog.stac_version == '0.7.0':
            filter['time'] = datetime

    retval = service.collection(collection_id).get_items(filter=filter)

    print(json.dumps(retval, indent=2))

@click.command()
@click.option('--url', default=None, help='The STAC server address (an URL).')
@click.option('--collections', default=None, help='Array of Collection IDs to include in the search for items.'\
              'Only Items in one of the provided Collections will be searched')
@click.option('--ids', default=None, help='Array of Item ids to return. All other filter parameters '\
                                          'that further restrict the number of search results '\
                                          '(except next and limit) are ignored')
@click.option('--intersects', default=None, help='Searches items by performing intersection between their '\
                                                 'geometry and provided GeoJSON Feature')
@click.option('--limit', default=10, help='The maximum number of results to return (page size). Defaults to 10')
@click.option('--next', default=None, help='The token to retrieve the next set of results, e.g., '\
                                        'offset, page, continuation token. (STAC 0.8.x only)')
@click.option('--page', default=1, help='The page number of results. Defaults to 1. (STAC 0.7.0 only)')
@click.option('--datetime', help='Single date, date+time, or a range (\'/\' seperator), formatted to RFC 3339, section 5.6')
@click.option('--bbox', default=None, help='Requested bounding box west, south, east, north')
@click.option('--access-token', default=None, help='Personal Access Token of the BDC Auth')
def search(url, collections, ids, intersects, limit, next, page, datetime, bbox, access_token=None):
    """Search through a STAC catalog."""
    service = STAC(url, access_token=access_token)
    service.catalog

    filter = {
        'limit': limit,
    }

    if service._catalog.stac_version == '0.8.0':
        if next is not None:
            filter['next'] = next
        if datetime is not None:
            filter['datetime'] = datetime
    elif service._catalog.stac_version == '0.7.0':
        if datetime is not None:
            filter['time'] = datetime


    if bbox is not None:
        filter['bbox'] = bbox
    if collections is not None:
        filter['collections'] = collections
    if intersects is not None:
        filter['intersects'] = intersects
    if ids is not None:
        filter['ids'] = ids

    retval = service.search(filter=filter)

    print(json.dumps(retval, indent=2))

cli.add_command(catalog)
cli.add_command(collection)
cli.add_command(items)
cli.add_command(search)
