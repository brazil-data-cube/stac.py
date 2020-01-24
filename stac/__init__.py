#
# This file is part of Python Client Library for STAC.
# Copyright (C) 2019 INPE.
#
# Python Client Library for STAC is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Python Client Library for STAC."""

from .stac import STAC
from .catalog import Catalog
from .collection import Collection, Provider, Extent, SpatialExtent, TemporalExtent
from .item import Item, ItemCollection, Geometry
from .link import Link
from .version import __version__

__all__ = ('__version__',
           'stac', )
