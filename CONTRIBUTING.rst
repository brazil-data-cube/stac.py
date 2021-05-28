..
    This file is part of Python Client Library for STAC.
    Copyright (C) 2019-2021 INPE.

    Python Client Library for STAC is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


Contributing
------------

Clone the Software Repository
+++++++++++++++++++++++++++++


Use ``git`` to clone the software repository::

    git clone https://github.com/brazil-data-cube/stac.py.git


Install ``stac.py`` in Development Mode
+++++++++++++++++++++++++++++++++++++++


Go to the source code folder::

    cd stac.py


Install in development mode::

    pip3 install -e .[all]


.. note::

    If you want to create a new *Python Virtual Environment*, please, follow this instruction:

    *1.* Create a new virtual environment linked to Python 3.7::

        python3.7 -m venv venv


    **2.** Activate the new environment::

        source venv/bin/activate


    **3.** Update pip and setuptools::

        pip3 install --upgrade pip

        pip3 install --upgrade setuptools


Run the Tests
+++++++++++++


Run the tests::

    ./run-tests.sh


Build the Documentation
+++++++++++++++++++++++


Generate the documentation::

    python setup.py build_sphinx


The above command will generate the documentation in HTML and it will place it under::

    docs/sphinx/_build/html/


You can open the above documentation in your favorite browser, as::

    firefox docs/sphinx/_build/html/index.html
