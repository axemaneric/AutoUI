# coding=utf-8
__author__ = "Eric"

# Test script for Friends feature in top bar.

import time

from testflow.lib.case.basecase import QuirkCase
from poco.drivers.unity3d import UnityPoco
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

from airtest.core.api import *


class Friends(QuirkCase):

    @classmethod
    def setUpClass(cls):
        super(Friends, cls).setUpClass()
        cls.installQuirk()
        cls.createAvatar()

    def setUp(self):
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

    def referTest(self):
        self.poco("invite_a_friend").click()
        # snapshot('../../res/img/friends/invite.jpg')
        with self.subTest(page="invite_a_friend"):
            assert_exists(Template(self.R('res/img/friends/invite.jpg')),
                          "Did not load into invite friends")
        with self.subTest(page="invite_a_friend"):
            self.assertTrue(self.poco("send_an_invitation").exists(),
                            "Send invitation button does not exist")

    def menuTest(self):
        self.poco("friends").click()
        with self.subTest(page="friends"):
            assert_exists(Template(self.R('res/img/friends/main.jpg')),
                          "Friends main menu did not open")
        self.poco("exit_container").click()
        assert_exists(Template(self.R('res/img/Commons.jpg')),
                      "Failed to return to Commons")

    def runTest(self):
        self.recentsTest()
        self.referTest()
        self.menuTest()


if __name__ == '__main__':
    import pocounit
    pocounit.main()
