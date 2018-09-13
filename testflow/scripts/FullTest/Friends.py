# coding=utf-8
__author__ = "Eric"

# Test script for Friends feature in top bar. Tests if all tabs in friends
# are accessible and contains all UI elements. Recent_friends tab is a bad
# test: refer to recentsTest()

import time

from testflow.lib.case.basecase import QuirkCase
from poco.drivers.unity3d import UnityPoco
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

from airtest.core.api import *


#--------------------------------------------------------------------#
#   TEST CASE                                                        #
#--------------------------------------------------------------------#
# BEGIN -> Enter friends menu -> Check in main -> Click Recents ->
# If players exist, check if player card exists in menu, otherwise skip ->
# Click invite friend menu -> check if UI elements exist
class Friends(QuirkCase):

    def setUp(self):
        self.createAvatar()
        self.poco("friends").click()
        # snapshot("../../res/img/friends/main.jpg")

    # High chances of not meeting a player in env, so recent_tests is very basic
    # Can uncomment section if players can be met in testing environment to
    # test for recent players showing up in friends menu
    def recentsTest(self):
        self.poco("recent_players").click()
        # snapshot('../../res/img/friends/recents.jpg')
        with self.subTest(page="recent_players"):
            assert_exists(Template(self.R('res/img/friends/recents.jpg')),
                          "Did not load into recents")
        # with self.subTest(page="recent_players"):
        #     self.assertTrue(self.poco("recent_player(Clone)").exists(),
        #                     "Missing friends card")
        # with self.subTest(page="recent_players"):
        #     self.assertTrue(self.poco("input").exists(),
        #                     "Friend search does not exists")

    # check if refer page appears and has relevant UI
    def referTest(self):
        self.poco("invite_a_friend").click()
        # snapshot('../../res/img/friends/invite.jpg')
        with self.subTest(page="invite_a_friend"):
            assert_exists(Template(self.R('res/img/friends/invite.jpg')),
                          "Did not load into invite friends")
        with self.subTest(page="invite_a_friend"):
            self.assertTrue(self.poco("send_an_invitation").exists(),
                            "Send invitation button does not exist")

    # return to main friends menu
    def menuTest(self):
        self.poco("friends").click()
        with self.subTest(page="friends"):
            assert_exists(Template(self.R('res/img/friends/main.jpg')),
                          "Friends main menu did not open")
        self.poco("exit_container").click()
        assert_exists(Template(self.R('res/img/Commons.jpg')),
                      "Failed to return to Commons")

    def runTest(self):
        assert_exists(Template(self.R('res/img/friends/main.jpg')))
        self.recentsTest()
        self.referTest()
        self.menuTest()


if __name__ == '__main__':
    import pocounit
    pocounit.main()
