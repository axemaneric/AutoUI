# coding=utf-8
__author__ = "Eric"

# Test script that runs all tests.

import time

from testflow.lib.case.basecase import QuirkCase
from testflow.lib.case.suite import QuirkSuite

from testflow.scripts.CreateAvatar import *
from testflow.scripts.Currency import *

if __name__ == '__main__':
    suite = QuirkSuite([
        Credits(),
        Crystals(),
        NameChange()
    ])
    import pocounit
    pocounit.run(suite)
