# coding=utf-8
__author__ = "Eric"

import time

from testflow.lib.case.unity_game import QuirkCase
from testflow.lib.utils.installation import install_android_app
from poco.drivers.unity3d import UnityPoco
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from poco.exceptions import InvalidOperationException
from pocounit.suite import PocoTestSuite

from airtest.core.api import device as current_device, connect_device
from airtest.core.api import *


class OptionsMenu(QuirkCase):

    # @classmethod
    # def setUpClass(cls):
    #     pass

    def setUp(self):
        self.maxDiff = None
        self.assertErrors = []
        self.poco = UnityPoco()
        self.poco("OptionsButton").click()

    def slideLeft(self, option_name):
        bar = self.poco(option_name).child(
            "background").child("slider").child("background")
        handle = self.poco(option_name).child("background").child(
            "slider").child("handle_slider_container").child("handle")
        handle.drag_to(bar.focus([0, 0.5]))

    def clickAll(self, option_name):
        graphic_options = self.poco(option_name).offspring("options_container")

        index = 0
        for option in graphic_options.children():
            option.click()
            # snapshot('../../res/img/optionsmenu/grahpics/' + str(index) + '.png')
            index += 1

    # def testInstances(self):

    def testAgeVerify(self):
        self.poco("age_verified").offspring("background_b").click()
        self.assertTrue(exists(Template(self.R(
            'res/img/optionsmenu/age_verify.png'))), "Age verification screen not found")
        self.poco("help").click()
        self.assertTrue(exists(
            Template(self.R('res/img/optionsmenu/age_help.png'))),
            "Help screen not found")
        self.poco("back").click()
        self.poco("of_age").click()
        self.poco("too_young").click()
        self.poco("continue").click()
        self.assertTrue(exists(Template(self.R(
            'res/img/optionsmenu/parental_consent.png'))), "Parent consent sreen not found")
        self.poco("not_now").click()
        self.assertTrue(exists(Template(self.R(
            'res/img/optionsmenu/parent_unavailable.png'))), "Parent availability screen not found")
        self.poco("back").click()
        self.poco("i_am_a_parent").click()
        self.assertTrue(exists(Template(self.R(
            'res/img/optionsmenu/parent_verification.png'))), "Parent verification screen not found")
        self.poco("not_now").click()
        self.poco("okay").click()
        # self.poco("continue").click()
        # self.assertTrue(self.poco("verified").exists())

    def testLinkGoogle(self):
        print("Switching to android poco")
        self.poco = AndroidUiautomationPoco()
        for x in range(0, 3):
            self.poco("com.google.android.gms:id/account_profile_picture").click()
            time.sleep(1)
        self.assertTrue(exists(Template(self.R(
            'res/img/optionsmenu/fail_authenticate.png'))), "Fail authentication screen not found")
        print("Switching to unity poco")
        self.poco = UnityPoco()
        self.poco("Accept").click()

    def runTest(self):
        self.assertTrue(
            exists(Template(self.R('res/img/options.png'))),
            "Options menu not found")

        all_options = self.poco("content")
        scrollview = self.poco("scroll_view")
        special_options = ["info", "restore_defaults", "blocked_players",
                           "link_google", "age_verified", "instances", "terms"]

        for option in all_options.children():
            option_name = option.get_name()
            self.scrollDownClick(scrollview, option_name)
            if not option_name.endswith("header") and option_name not in special_options:
                if option.offspring("slider").exists():
                    self.slideLeft(option_name)
                elif option.offspring("true").exists():
                    self.poco(option_name).offspring("false").click()
                elif option.offspring("options_container").exists():
                    self.clickAll(option_name)
                snapshot(self.R('res/img/optionsmenu/' + option_name + '.png'))
                self.check(Template(self.R('res/img/optionsmenu/' + option_name + '.png')), "" + option_name + " option may contain errors")
            elif option_name == "restore_defaults":
                # scrollDownClick clicks onto restore defaults button
                if self.check(Template(self.R('res/img/optionsmenu/restore_defaults.png')), "Restore default screen not found"):
                    self.poco("Accept").click()
            elif option_name == "blocked_players":
                # scrollDownclick clicks onto blocked_players button
                if self.check(Template(self.R('res/img/optionsmenu/blockedplayers.png')), "Blocked players screen not found"):
                    self.poco("exit_container").click()
            elif option_name == "link_google":
                time.sleep(10)
                if self.check(Template(self.R('res/img/optionsmenu/link_google.png')), "Google verification screen not found"):
                    self.testLinkGoogle()
            elif option_name == "age_verified":
                if self.check(Template(self.R('res/img/optionsmenu/age_verify.png')), "Age verification screen not found"):
                    self.testAgeVerify()
            # elif option_name = "instances":
            #     self.testInstances()
            elif option_name == "terms":
                terms = self.poco("terms").child("background").children()
                for term in terms:
                    term.click()
                    self.check(Template(self.R(
                        'res/img/optionsmenu/' + term.get_name() + '.png')), "Failed to find: " + term.get_name())
                    self.poco("exit_container").click()

    def tearDown(self):
        self.assertEqual([], self.assertErrors)
        # @classmethod
        # def tearDownClass(cls):
        #     pass


if __name__ == '__main__':
    import pocounit
    pocounit.main()
