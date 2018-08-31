# coding=utf-8
__author__ = "Eric"

# Test script for initial avatar customization phase using test suite.
# Resets Avatar manually to default colors. Does not reset QUIRK
# between tests.

from testflow.lib.case.basecase import QuirkCase
from testflow.lib.utils.installation import install_android_app
from poco.drivers.unity3d import UnityPoco
from poco.exceptions import InvalidOperationException
from pocounit.suite import PocoTestSuite

from airtest.core.api import device as current_device, connect_device
from airtest.core.api import *

#--------------------------------------------------------------------#
#   TESTFLOW                                                         #
#--------------------------------------------------------------------#

#   BEGIN (Installation) -> SIMPLETEST (Zoom in/Zoom out/Color
#   change) -> COLORTOGGLE (Clicks every color for skin and hair) ->
#   SELECTIONTEST (Navigates through left side bar and clicks on every
#   element in main screen) -> RANDOMIZETEST (Clicks on randomize and
#   see if it can discard changes) -> ACCOUNTCREATION (Creates account
#   with default username and checks if hamburger menu is functional)
#   -> END


#--------------------------------------------------------------------#
#   TEST SUITE                                                       #
#--------------------------------------------------------------------#
# sets up a suite of test cases for Avatar Customization
class AvatarCustomizationSuite(PocoTestSuite):

    def setUp(self):
        if not current_device():
            connect_device('Android:///')

        self.package_name = 'com.ugen.playquirk'
        apk_path = self.R('res/app/quirk.apk')
        install_android_app(current_device().adb, apk_path)
        start_app(self.package_name)
        time.sleep(30)

    def tearDown(self):
        stop_app(self.package_name)
        uninstall(self.package_name)


#--------------------------------------------------------------------#
#   BASE CASE                                                        #
#--------------------------------------------------------------------#
# Checks if avatar resets and resets if not
class AvatarCustomizationCase(QuirkCase):

    @classmethod
    def tearDownClass(cls):
        super(QuirkCase, cls).tearDownClass()

    def colorToggleScrollUp(self):
        print("Scrolling up...")
        start = self.poco("ContentGrid").child(
            "CatalogItemDisplayMobile(Clone)")[12].child("Background")
        stop = self.poco("ContentGrid").child(
            "CatalogItemDisplayMobile(Clone)")[22].child("Background")
        start.drag_to(stop)

    def setUp(self):
        self.poco = UnityPoco()

        print("Checking for change...")

        AvatarHead = Template(self.R('res/img/default-avatar.png'),
                              rgb=True, threshold=0.9)
        AvatarMenu = Template(self.R('res/img/default.png'), rgb=True,
                              threshold=0.9)
        if not exists(AvatarMenu) or not exists(AvatarHead):
            try:
                self.poco("ColorToggle").click()
            except InvalidOperationException:
                nav_bar = self.poco("SalonNavbarMobile(Clone)")
                print("Scrolling nav bar...")
                nav_bar.focus([0.5, 0.2]).drag_to(nav_bar.focus([0.5, 0.8]))
                nav_bar.focus([0.5, 0.2]).drag_to(nav_bar.focus([0.5, 0.8]))
                nav_bar.focus([0.5, 0.2]).drag_to(nav_bar.focus([0.5, 0.8]))
                self.poco("ColorToggle").click()
            finally:
                self.poco("SkinToggle").click()
                self.colorToggleScrollUp()
                self.poco("ContentGrid").child("CatalogItemDisplayMobile(Clone)")[
                    2].child("Background").click()
                self.poco("HairToggle").click()
                self.poco("ContentGrid").child("CatalogItemDisplayMobile(Clone)")[
                    5].child("Background").click()


#--------------------------------------------------------------------#
#   TEST CASES                                                       #
#--------------------------------------------------------------------#


# Tests zoom in/zoom out button and a simple color change for hair and skin
class SimpleTest(AvatarCustomizationCase):

    def runTest(self):

        AvatarMenu = Template(self.R('res/img/default.png'), rgb=True)
        wait(AvatarMenu)
        print('Loaded into avatar customization')

        self.poco("ZoomInButton").child("Button").click()
        self.poco("ZoomOutButton").child("Button").click()

        self.poco("OptionsButton").click()
        self.assertTrue(
            exists(Template(self.R('res/img/options.png'))), "Failed to enter optionsmenu")
        self.poco("exit_container").click()

        self.poco("SkinToggle").click()
        start = self.poco("ContentGrid").child(
            "CatalogItemDisplayMobile(Clone)")[12].child("Background")

        stop = self.poco("ContentGrid").child(
            "CatalogItemDisplayMobile(Clone)")[2].child("Background")

        start.drag_to(stop)

        self.poco("ContentGrid").child("CatalogItemDisplayMobile(Clone)")[
            23].child("Background").click()

        self.poco("HairToggle").click()
        self.poco("ContentGrid").child("CatalogItemDisplayMobile(Clone)")[
            23].child("Background").click()

        ChangedAvatar = Template(self.R('res/img/endresult.png'))
        self.assertTrue(exists(ChangedAvatar), 'Test failed')


# Full skin and hair color toggle test
# Set recapture to true to recapture screenshots used to assert changes
class ColorToggleTest(AvatarCustomizationCase):

    def helper(self, toggle, scroll=False, recapture=False):

        self.poco(toggle).click()
        content_grid = self.poco("ContentGrid").children()
        if scroll:
            self.colorToggleScrollUp()
        index = 1
        for catalog_items in content_grid:
            try:
                catalog_items.child("Background").click()
            except InvalidOperationException:
                start = self.poco("ContentGrid").child(
                    "CatalogItemDisplayMobile(Clone)")[12].child("Background")
                stop = self.poco("ContentGrid").child(
                    "CatalogItemDisplayMobile(Clone)")[2].child("Background")
                start.drag_to(stop)
                catalog_items.child("Background").click()
            finally:
                if recapture:
                    snapshot("../../res/img/Avatar/ColorToggle/" +
                             toggle + "/" + str(index) + ".png")
                self.assertTrue(exists(Template(self.R(
                    "res/img/Avatar/ColorToggle/" + toggle + "/" + str(index) + ".png"), rgb=True, threshold=0.9)))

            index += 1

    def runTest(self):

        self.helper("SkinToggle")
        self.helper("HairToggle", scroll=True)


# Full navigation bar and content test
# Set recapture to true to recapture screenshots used to assert changes
class SelectionTest(AvatarCustomizationCase):

    def helper(self, recapture=False):

        nav_bar = self.poco("SalonNavbarMobile(Clone)")
        nav_bar_children = self.poco("ToggleGroup").children()
        for toggle in nav_bar_children:
            name = toggle.get_name()
            if name != "Margin" and name != "ColorToggle":
                try:
                    print("Testing... " + name)
                    self.poco(name).click()
                except InvalidOperationException:
                    print("Scrolling nav bar...")
                    nav_bar.focus([0.5, 0.8]).drag_to(
                        nav_bar.focus([0.5, 0.2]))
                    self.poco(name).click()
                finally:
                    if self.poco("ContentGrid").exists():
                        content_grid = self.poco("ContentGrid")
                        content_grid_children = content_grid.children()
                        index = 1
                        for catalog_items in content_grid_children:
                            try:
                                catalog_items.child("Background").click()
                            except InvalidOperationException:
                                print('Scrolling...')
                                content_grid.focus([0.5, 0.8]).drag_to(
                                    content_grid.focus([0.5, 0.2]))
                                catalog_items.child("Background").click()
                            finally:
                                if recapture:
                                    snapshot("../../res/img/Avatar/" +
                                             name + "/" + str(index) + ".png")
                                self.assertTrue(exists(Template(self.R(
                                    "res/img/Avatar/" + name + "/" + str(index) + ".png"), rgb=True, threshold=0.9)))
                            index += 1

    def runTest(self):

        self.helper()

        # Tests the randomize button and discard changes screen


class RandomizeTest(AvatarCustomizationCase):

    def runTest(self):

        self.poco("SwapAvatar").child(type="Button").click()
        snapshot('../../res/img/discardconfirm.png')
        self.assertTrue(exists(
            Template(self.R('res/img/discardconfirm.png'))), "Avatar has not been editted")
        self.poco("Accept").click()
        # assert avatar changed
        self.poco("SwapAvatar").child(type="Button").click()
        self.assertFalse(exists(Template(
            self.R('res/img/discardconfirm.png'))), "Discard image screen appeared")


# Tests whether avatar account can be created
class FinishTest(AvatarCustomizationCase):

    def runTest(self):
        self.createAvatar()


if __name__ == '__main__':
    suite = AvatarCustomizationSuite([
        SimpleTest(),
        ColorToggleTest(),
        SelectionTest(),
        RandomizeTest(),
        FinishTest()
    ])
    import pocounit
    pocounit.run(suite)
