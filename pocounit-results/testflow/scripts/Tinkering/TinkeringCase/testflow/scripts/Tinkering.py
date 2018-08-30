# coding=utf-8
__author__ = "Eric"
# Test script used for testing tinkering menu. Loads into tinkering menu and
# clicks on modify, then clicking all possible elements, viewing weapon info
# and then returning to select the next weapon. Runs a full test and then
# outputs all test failures at end of test as a failure list.


from testflow.lib.case.unity_game import QuirkCase
from testflow.lib.utils.installation import install_android_app
from poco.drivers.unity3d import UnityPoco
from poco.exceptions import InvalidOperationException
from pocounit.suite import PocoTestSuite

from airtest.core.api import device as current_device, connect_device
from airtest.core.api import *

#--------------------------------------------------------------------#
#   TEST CASE                                                        #
#--------------------------------------------------------------------#


class TinkeringCase(QuirkCase):

    def setUp(self):
        self.maxDiff = None
        self.assertErrors = []

    def runTest(self):
        self.poco("quick_menu_button").click()
        self.poco("tinkering").click()
        time.sleep(5)

        self.check(Template(self.R('res/img/tinkering/main.png')),
                   "Failed to enter tinkering screen")

        weapon_list = self.poco("VerticalLayoutGroup").children()
        weapon_id = ["hammer", "potato", "rocket", "toastilizer"]

        weapon_index = 0
        for weapon in weapon_list:
            name = weapon_id[weapon_index]
            address_base = 'res/img/tinkering/' + name + '/' + name

            weapon.click()
            snapshot('../../' + address_base + '.png')
            self.check(Template(self.R(address_base + '.png')),
                       "Failed to switch weapon: " + name)

            self.poco("ModifyLabel").click()
            # snapshot('../../' + address_base + '_modify.png')
            self.check(Template(self.R(address_base + '_modify.png')),
                       "Failed to enter modify screen: " + name)

            loadout_list = self.poco("BottomButtons").children()

            if weapon_index == 0:
                weapon_loadout = ["head", "body", "handle"]
            else:
                weapon_loadout = ["ammo", "barrel", "body", "stock"]

            loadout_index = 0
            for loadout in loadout_list:
                loadout_name = weapon_loadout[loadout_index]
                new_base = address_base + '_' + loadout_name
                errortag = name + ": " + loadout_name

                loadout.click()
                # snapshot('../../' + new_base + '.png')
                self.check(Template(self.R(new_base + '.png')),
                           "Failed to switch part: " + errortag)

                self.poco("InfoButton").click()
                # snapshot('../../' + new_base + '_info.png')
                self.check(Template(self.R(new_base + '_info.png')),
                           "Failed to enter info screen: " + errortag)

                self.poco("PartUpgradePanel(Clone)").child(
                    "ExitButton").click()
                loadout_index += 1

            self.poco("BackButton").click()
            weapon_index += 1

        self.poco("TinkeringMainPanel(Clone)").child("ExitButton").click()
        time.sleep(10)
        self.check(Template(self.R('res/img/Commons.png')),
                   "Failed to return to Commons")

    # Outputs all assertion errors in list assertErrors
    def tearDown(self):
        self.assertEqual([], self.assertErrors)


if __name__ == '__main__':
    import pocounit
    pocounit.main()
