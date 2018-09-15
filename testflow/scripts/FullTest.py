# coding=utf-8
__author__ = "Eric"

# Test script that runs all tests.

import time

from testflow.lib.case.basecase import QuirkCase
from testflow.lib.case.suite import QuirkSuite

from testflow.scripts.CreateAvatar import *
from testflow.scripts.Currency import *
from testflow.scripts.Avatar import *
from testflow.scripts.BuildMenu import *
from testflow.scripts.Chat import *
from testflow.scripts.Emoji import *
from testflow.scripts.MenuBar import *
from testflow.scripts.OptionsMenu import *
from testflow.scripts.OvermapTravel import *
from testflow.scripts.QuestsTab import *
from testflow.scripts.Selfie import *
from testflow.scripts.Tokens import *
from testflow.scripts.Tinkering import *

if __name__ == '__main__':
    suite = QuirkSuite([
        # SimpleTest(),
        # RandomizeTest(),
        # FinishTest(),
        # # AllMenu(),
        Credits()
        # Crystals(),
        # NameChange(),
    ])
    import pocounit
    pocounit.run(suite)
