#
# This file is part of Python Client Library for STAC.
# Copyright (C) 2019 INPE.
#
# Python Client Library for STAC is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Command line interface for the STAC client."""

from pprint import pprint

import click

from .stac import stac


@click.group()
def cli():
    """STAC on command line."""
    pass


@click.command()
@click.option('--url', default=None, help='The STAC server address (an URL).')
def conformance(url):
    """Return the list of conformance classes that the server conforms to."""
    service = stac(url)

    retval = service.conformance()

    pprint(retval)


cli.add_command(conformance)