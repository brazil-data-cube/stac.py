..
    This file is part of Python Client Library for STAC.
    Copyright (C) 2019-2021 INPE.

    Python Client Library for STAC is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


==============================
Python Client Library for STAC
==============================


.. image:: https://img.shields.io/badge/license-MIT-green
        :target: https://github.com//brazil-data-cube/stac.py/blob/master/LICENSE
        :alt: Software License


.. image:: https://drone.dpi.inpe.br/api/badges/brazil-data-cube/stac.py/status.svg
        :target: https://drone.dpi.inpe.br/api/badges/brazil-data-cube/stac.py
        :alt: Build Status


.. image:: https://codecov.io/gh/brazil-data-cube/stac.py/branch/master/graph/badge.svg?token=WWQ3HQAUKK
        :target: https://codecov.io/gh/brazil-data-cube/stac.py
        :alt: Code Coverage


.. image:: https://readthedocs.org/projects/stacpy/badge/?version=latest
        :target: https://stacpy.readthedocs.io/en/latest/
        :alt: Documentation Status


.. image:: https://img.shields.io/badge/lifecycle-maturing-blue.svg
        :target: https://www.tidyverse.org/lifecycle/#maturing
        :alt: Software Life Cycle


.. image:: https://img.shields.io/github/tag/brazil-data-cube/stac.py.svg
        :target: https://github.com/brazil-data-cube/stac.py/releases
        :alt: Release


.. image:: https://img.shields.io/pypi/v/stac.py
        :target: https://pypi.org/project/stac.py/
        :alt: Release


.. image:: https://img.shields.io/discord/689541907621085198?logo=discord&logoColor=ffffff&color=7389D8
        :target: https://discord.com/channels/689541907621085198#
        :alt: Join us at Discord

.. image:: https://mybinder.org/badge_logo.svg
        :target: https://mybinder.org/v2/gh/cedadev/stac.py/usage-notebook?filepath=examples%2Fusage.ipynb
        :alt: Binder interactive notebook

About
=====


``stac.py`` is a Python client API for the `SpatioTemporal Asset Catalog (STAC) specification <https://github.com/radiantearth/stac-spec>`_. The client library supports version ``0.7.0``, ``0.8.0``, ``0.8.1``, and ``0.9.0`` of the STAC API. Nevertheless, we aim to support new versions of the API in future releases of ``stac.py``. See the `milestones <https://github.com/brazil-data-cube/stac.py/milestones>`_ to get the list of versions planned in each release.


Installation
============


To install ``stac.py`` under your virtualenv, ensure you have the latest setuptools::

    pip install -U setuptools

Then::

    pip install stac.py

If you want rasterio support::

    pip install stac.py[geo]

For development version::

    pip install https://github.com/brazil-data-cube/stac.py/tarball/master


Usage
=====

Below is a quick example on how to use ```stac.py``.

.. code-block:: python

    from stac import STAC

    service = stac.STAC("https://brazildatacube.dpi.inpe.br/stac", access_token="your-token")

    print(service.catalog) # show all available collections

    collection = service.collections('CB4_64_16D_STK') # get a collection

    items = collection.get_items() # get the collection items

    arr = items[0].read("BAND14") # read the asset 'BAND14' from the first item as a numpy array.


For more information take a look at our `Documentation <https://stacpy.readthedocs/en/latest/>`_ page.

Developer Documentation
=======================


See `CONTRIBUTING <CONTRIBUTING.rst>`_.


License
=======


.. admonition::
    Copyright (C) 2019-2021 INPE.

    Python Client Library for STAC is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.
