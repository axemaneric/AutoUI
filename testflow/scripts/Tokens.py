# coding=utf-8
__author__ = "Eric"

# Test script for Tokens feature in top bar. Tests if token pouch can be
# accessed, uses token on machine, and tests if token has been used.
# THIS SCRIPT USES 'MANUAL' JOYSTICK MOVEMENT: tests have moderate chances of
# failure since character spawn location isn't constant

import time

from testflow.lib.case.basecase import QuirkCase
from testflow.lib.utils.installation import *

from poco.drivers.unity3d import UnityPoco

from airtest.core.api import *


#--------------------------------------------------------------------#
#   TEST CASE                                                        #
#--------------------------------------------------------------------#
class Tokens(QuirkCase):

    @classmethod
    def setUpClass(cls):
        super(Tokens, cls).setUpClass()
        cls.installQuirk()
        cls.createAvatar()

    def pouchBefore(self):
        self.poco("tokens").click()
        snapshot('../../res/img/tokens/main.jpg')
        assert_exists(Template(self.R('res/img/tokens/main.jpg')),
                      "Tokens pouch did not show up")
        self.poco("ExitContainer").click()

    def useMachine(self):
        joystick = self.poco("VirtualJoystick")
        joystick.focus([0.2, 0.2]).start_gesture().hold(
            1).to(joystick.focus([0.8, 0.2])).hold(2.35).up()
        if not (exists(Template(self.R('res/img/tokens/machine.jpg'), rgb=True, threshold=0.7)) or exists(Template(self.R('res/img/tokens/machine2.jpg'), rgb=True, threshold=0.7))):
            joystick.focus([0.5, 0.5]).drag_to(
                joystick.focus([0.6, 0.5]), duration=0.65)
            joystick.focus([0.2, 0.2]).start_gesture().hold(
                1).to(joystick.focus([0.8, 0.2])).hold(0.5).up()
        self.poco("ActionButton").click()

        self.assertTrue(self.poco("RectangleBackgroundSolidImage").exists(),
                        "Token insert tab did not pop up or failed to walk to slot machine")
        self.poco("TokenButton1").click()
        time.sleep(20)
        snapshot('../../res/img/tokens/rewards.jpg')
        assert_exists(Template(self.R('res/img/tokens/rewards.jpg')),
                      "Collect loot menu failed to show")

        rewards = self.poco("RewardContent")
        help_btn = self.poco("HelpButton")
        collect_btn = self.poco("Collect")
        self.assertTrue(rewards.exists() and help_btn.exists()
                        and collect_btn.exists(),
                        "Loot screen UI elements are missing")
        collect_btn.click()
        time.sleep(1)
        self.poco("CloseButton").click()
        self.assertFalse(self.poco("RectangleBackgroundSolidImage").exists(),
                         "Token insert tab failed to hide")

    def pouchAfter(self):
        self.poco("tokens").click()
        snapshot('../../res/img/tokens/after.jpg')
        assert_exists(Template(self.R('res/img/tokens/after.jpg')),
                      "Token has not been used")
        self.poco("ExitContainer").click()

    # the menu button blocks the exit button in help screen in current build so
    # it is not tested
    def runTest(self):
        self.poco = UnityPoco()
        self.pouchBefore()
        self.useMachine()
        self.pouchAfter()

        # self.poco("HelpButton").click()
        # snapshot('../../res/img/tokens/help.jpg')
        # assert_exists(Template(self.R('res/img/tokens/help.jpg')),
        #               "Help screen did not show up")


if __name__ == '__main__':
    import pocounit
    pocounit.main()
