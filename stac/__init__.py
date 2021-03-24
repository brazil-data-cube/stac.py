#
# This file is part of Python Client Library for STAC.
# Copyright (C) 2019-2021 INPE.
#
# Python Client Library for STAC is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Python Client Library for STAC."""

from . import cli
from .catalog import Catalog
from .collection import Collection, Extent, Provider
from .common import Link
from .item import Geometry, Item, ItemCollection
from .stac import STAC
from .utils import Utils
from .version import __version__

__all__ = ('__version__',
           'stac', )
