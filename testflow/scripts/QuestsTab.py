# coding=utf-8
__author__ = "Eric"

# Test script for Quests function in top bar of Quirk.

import time

from testflow.lib.case.basecase import QuirkCase
from poco.exceptions import PocoNoSuchNodeException

from airtest.core.api import *


#--------------------------------------------------------------------#
#   TESTFLOW                                                         #
#--------------------------------------------------------------------#

# BEGIN: Quests page -> claimRewardsTest-> swipeRightTest -> replaceQuestsTest
# -> END
# Refer to individual methods for individual test breakdown

#--------------------------------------------------------------------#
#   TESTCASE                                                         #
#--------------------------------------------------------------------#
class QuestsTab(QuirkCase):

    # install Quirk and generate a default avatar
    @classmethod
    def setUpClass(cls):
        super(QuestsTab, cls).setUpClass()
        cls.installQuirk()
        cls.createAvatar()

    def setUp(self):
        self.poco("daily_quests").click()

    # check if initial state is Quest page then run tests in order
    def runTest(self):
        # snapshot('../../res/img/quests.png')
        self.assertTrue(
            exists(Template(self.R('res/img/quests.png'))), "Quests page not found")
        self.claimRewardsTest()
        self.swipeRightTest()
        self.replaceQuestsTest()

    # to test if quests page has more quests on the right
    # by swipe right and assert change
    def swipeRightTest(self):
        viewport = self.poco("viewport")
        viewport.focus([0.8, 0.5]).drag_to(viewport.focus([0.2, 0.5]))
        # snapshot('../../res/img/queststab/after_swipe.png')
        self.assertTrue(
            exists(Template(self.R('res/img/queststab/after_swipe.png'))), "Swipe right failed")

    # Tests if Avatar shop reward can be claimed
    # BEGIN: Quests page -> Exit to Commons -> Access Avatar through MenuBar ->
    # Enter Avatar Saloon -> Exit to Commons -> Open Quests page -> Check if
    # Avatar Visit quest is claimable -> Claim rewards -> Check if rewards
    # have been recieved -> END
    def claimRewardsTest(self):

        self.poco("exit_container").click()
        self.poco("quick_menu_button").click()
        self.poco("avatar").click()
        time.sleep(5)
        self.assertTrue(exists(Template(self.R('res/img/avatar.png'))),
                        "Avatar customization screen not found")
        self.poco("DismissButton").click()
        time.sleep(10)
        self.poco("daily_quests").click()
        # assert false
        # snapshot('../../res/img/queststab/reward.png')
        self.assertTrue(exists(Template(
            self.R('res/img/queststab/reward.png'))), "No rewards available to be claimed")
        claim = self.poco("claim")
        self.assertTrue(claim.exists(), "Claim rewards button does not exists")
        claim.click()
        # snapshot("../../res/img/queststab/after_claim.png")
        self.assertTrue(exists(Template(
            self.R('res/img/queststab/after_claim.png'))), "Failed to claim rewards")
        # snapshot("../../res/img/queststab/150.png")
        self.assertTrue(exists(
            Template(self.R('res/img/queststab/150.png'))), "Gold value did not change")

    # Test for checking if replacing quests work
    # BEGIN: Quests page -> Find nearest Dismiss button -> Replace quest ->
    # Repeat until no more Dismiss button exists -> Check if number of quests
    # replaced equals allowed amount (default is 3)
    def replaceQuestsTest(self, dismisses_allowed=3):

        quests_dismissed = 0
        while self.poco("dismiss").exists():
            self.poco("dismiss").click()
            quests_dismissed += 1
            time.sleep(1)
        self.assertEqual(quests_dismissed, dismisses_allowed, "Actual dismisses not qual to allowed number of dismisses")

    def tearDown(self):
        self.poco("exit_container").click()


if __name__ == '__main__':
    import pocounit
    pocounit.main()