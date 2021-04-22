..
    This file is part of Python Client Library for STAC.
    Copyright (C) 2019-2021 INPE.

    Python Client Library for STAC is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


Changes
=======

Version 0.9.0-11 (2021-04-22)
-----------------------------

- Fix bug in /search using GET method (`#86 <https://github.com/brazil-data-cube/stac.py/issues/86>`_).


Version 0.9.0-10 (2021-04-09)
-----------------------------

- Fix stac_search using GET method with two collections (`#83 <https://github.com/brazil-data-cube/stac.py/issues/83>`_).


Version 0.9.0-9 (2021-03-29)
----------------------------

- Fix package installation, adding Shapely as required dependency (`#78 <https://github.com/brazil-data-cube/stac.py/issues/78>`_).


Version 0.9.0-8 (2021-03-24)
----------------------------

- Add common way for dealing with minimum bounding region in search (`#75 <https://github.com/brazil-data-cube/stac.py/issues/75>`_).


Version 0.9.0-7 (2021-03-24)
----------------------------


API improvements:

- Download all assets from an item (`#66 <https://github.com/brazil-data-cube/stac.py/issues/66>`_).

- Add a way for reading partial raster given an envelope in a specific CRS (`#71 <https://github.com/brazil-data-cube/stac.py/issues/71>`_).

- Fix download folder creation in asset (`#64 <https://github.com/brazil-data-cube/stac.py/issues/64>`_).

- Add Drone integration (`#60 <https://github.com/brazil-data-cube/stac.py/issues/60>`_).


Version 0.9.0-6 (2020-12-10)
----------------------------


- Add tqdm progress bar to asset download (`#52 <https://github.com/brazil-data-cube/stac.py/pull/52>`_).

- Add collections to stac (`#55 <https://github.com/brazil-data-cube/stac.py/issues/55>`_).


Version 0.9.0-5 (2020-09-22)
----------------------------


- Add feature iterator on ItemCollection (`#50 <https://github.com/brazil-data-cube/stac.py/pull/50>`_).

- Add function to read Item as numpy array (`#50 <https://github.com/brazil-data-cube/stac.py/pull/50>`_).


Version 0.9.0-4 (2020-09-15)
----------------------------


- Add Jupyter integration: `#47 <https://github.com/brazil-data-cube/stac.py/pull/47>`_.


Version 0.9.0-3 (2020-09-14)
----------------------------


- Publish into pypi (`#46 <https://github.com/brazil-data-cube/stac.py/pull/46>`_).


Version 0.9.0-2 (2020-09-10)
----------------------------


- Bug fix: properly handle query parameter (`#42 <https://github.com/brazil-data-cube/stac.py/issues/42>`_).


Version 0.9.0-1 (2020-09-01)
----------------------------


- Improved tests.


Version 0.9.0-0 (2020-09-01)
----------------------------


- Support for STAC version 0.9.0.

- Review of Sphinx project.


Version 0.8.1-0 (2020-04-14)
----------------------------


- Support for STAC version 0.8.1.

- Added tests for STAC version 0.8.1.


Version 0.8.0-0 (2020-04-03)
----------------------------


- Support for STAC version 0.8.0.

- Added tests for STAC version 0.8.0.

- Added CLI support.

- Added tests for CLI.

- Removed stac.collections property


Version 0.7.0-0 (2020-02-27)
----------------------------


- First experimental version.

- Support for STAC version 0.7.0.

- Documentation system based on Sphinx.

- Documentation integrated to ``Read the Docs``.

- Unit-tests with code coverage.

- Package support through Setuptools.

- Installation and use instructions.

- Source code versioning based on `Semantic Versioning 2.0.0 <https://semver.org/>`_.

- License: `MIT <https://github.com/brazil-data-cube/stac.py/blob/master/LICENSE>`_.
