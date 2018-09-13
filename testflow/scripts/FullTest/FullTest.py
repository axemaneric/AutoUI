# coding=utf-8
__author__ = "Eric"

# Test script that runs all tests.

import time

from testflow.lib.case.basecase import QuirkCase
from testflow.lib.case.suite import QuirkSuite

from testflow.scripts.FullTest.CreateAvatar import *
from testflow.scripts.FullTest.Currency import *


class Currency(QuirkCase):

    def setUp(self):
        pass


if __name__ == '__main__':
    suite = QuirkSuite([
        Credits(),
        Crystals(),
        NameChange()
    ])
    import pocounit
    pocounit.run(suite)
