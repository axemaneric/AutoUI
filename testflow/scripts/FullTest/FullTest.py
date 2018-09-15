# coding=utf-8
__author__ = "Eric"

# Test script that runs all tests.

import time

from testflow.lib.case.basecase import QuirkCase
from testflow.lib.case.suite import QuirkSuite

from testflow.scripts.FullTest.CreateAvatar import *
from testflow.scripts.FullTest.Currency import *
from testflow.scripts.FullTest.Avatar import *
from testflow.scripts.FullTest.BuildMenu import *
from testflow.scripts.FullTest.Chat import *
from testflow.scripts.FullTest.Emoji import *
from testflow.scripts.FullTest.MenuBar import *
from testflow.scripts.FullTest.OptionsMenu import *
from testflow.scripts.FullTest.OvermapTravel import *
from testflow.scripts.FullTest.QuestsTab import *
from testflow.scripts.FullTest.Selfie import *
from testflow.scripts.FullTest.Tokens import *
from testflow.scripts.FullTest.Tinkering import *


if __name__ == '__main__':
    suite = QuirkSuite([
        # OptionsMenu(),
        FinishTest(),
        # ChatYoung(),
        # EmojiChat(),
        # TutorialTest(),
        # SaveTest(),
        # Credits(),
        # Crystals(),
        # NameChange(),
        # Emoji(),
        # AllIcons(),
        # QuestsTab()
        Tokens()
    ])
    import pocounit
    pocounit.run(suite)
