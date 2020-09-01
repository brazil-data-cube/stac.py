#
# This file is part of Python Client Library for STAC.
# Copyright (C) 2019 INPE.
#
# Python Client Library for STAC is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Unit-test for stac.py."""
import pytest

if __name__ == '__main__':
    import stac_tests.test_stac
    pytest.main(['--color=auto', '--no-cov', '-v', '-x'])
