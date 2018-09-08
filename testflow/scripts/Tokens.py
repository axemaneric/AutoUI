# coding=utf-8
__author__ = "Eric"

# Test script for Friends feature in top bar.

import time

from testflow.lib.case.basecase import QuirkCase
from poco.drivers.unity3d import UnityPoco
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

from airtest.core.api import *


class Tokens(QuirkCase):

    @classmethod
    def setUpClass(cls):
        super(Tokens, cls).setUpClass()
        cls.installQuirk()
        cls.createAvatar()

    # the menu button blocks the exit button in help screen in current build
    def runTest(self):
        self.poco = UnityPoco()
        snapshot('../../res/img/Commons.jpg')
        self.assertTrue(exists(
            Template(self.R('res/img/Commons.jpg'), threshold=0.9)), "Too far or too near")
        # self.poco("tokens").click()
        # # snapshot('../../res/img/tokens/main.jpg')
        # # assert_exists(Template(self.R('res/img/tokens/main.jpg')),
        # #               "Tokens pouch did not show up")
        # self.poco("ExitContainer").click()
        joystick = self.poco("VirtualJoystick")
        joystick.focus([0.2, 0.2]).start_gesture().hold(
            1).to(joystick.focus([0.8, 0.2])).hold(2.5).up()
        if not (exists(Template(self.R('res/img/tokens/machine.jpg'), rgb=True, threshold=0.7)) or exists(Template(self.R('res/img/tokens/machine2.jpg'), rgb=True, threshold=0.7))):
            joystick.focus([0.5, 0.5]).drag_to(joystick.focus([0.6, 0.5]), duration=0.65)
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

        # self.poco("HelpButton").click()
        # snapshot('../../res/img/tokens/help.jpg')
        # assert_exists(Template(self.R('res/img/tokens/help.jpg')),
        #               "Help screen did not show up")

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == '__main__':
    import pocounit
    pocounit.main()
