# coding=utf-8
__author__ = "Eric"

# Test script for credits and crystals.

import time

from testflow.lib.case.basecase import QuirkCase
from poco.drivers.unity3d import UnityPoco
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

from airtest.core.api import *


#--------------------------------------------------------------------#
#   BASE CASE                                                        #
#--------------------------------------------------------------------#
class Currency(QuirkCase):

    def setUp(self):
        self.createAvatar()


#--------------------------------------------------------------------#
#   TEST CASES                                                       #
#--------------------------------------------------------------------#
# Goes into store and attempts to use 15 crystals to buy 250 credits
class Credits(Currency):

    def runTest(self):
        self.poco("credits").click()
        # snapshot('../../res/img/currency/credits.jpg')
        assert_exists(Template(self.R('res/img/currency/credits.jpg')),
                      "Not in credits menu")
        self.poco("Items").child(
            "CurrencyPurchasableDisplay(Clone)")[0].click()
        self.poco("Button").click()
        time.sleep(3)
        # snapshot('../../res/img/currency/350.jpg')
        assert_exists(Template(self.R('res/img/currency/350.jpg')),
                      "Crystals were not used to buy credits")


# Check if crystals icon leads to Crystals purchase screen
class Crystals(Currency):

    def runTest(self):
        self.poco("crystals").click()
        # snapshot('../../res/img/currency/crystals.jpg')
        assert_exists(Template(self.R('res/img/currency/crystals.jpg')),
                      "Not in crystals menu")

    def tearDown(self):
        self.poco("DismissButton").click()


# Tests if free name change feature is working
class NameChange(Currency):

    def setUp(self):
        super(NameChange, self).setUp()
        self.poco("credits").click()

    def runTest(self):
        self.assertTrue(self.poco("free_button").exists())
        self.poco("free_button").click()
        # snapshot('../../res/img/currency/name.jpg')
        assert_exists(Template(self.R('res/img/currency/name.jpg')),
                      "Name change screen did not show")
        self.poco("random_name").click()
        self.poco("save").click()
        # snapshot('../../res/img/currency/success.jpg')
        assert_exists(Template(self.R('res/img/currency/success.jpg')),
                      "Name change success screen did not show")
        self.poco("continue").click()


if __name__ == '__main__':
    import pocounit
    pocounit.main()
