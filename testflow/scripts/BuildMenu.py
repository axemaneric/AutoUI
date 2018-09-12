# coding=utf-8
__author__ = "Eric"

# Test script used for the BuildMenu. Clicks on every possible block and
# places them on canvas, checks, then resets for testing next block by clicking
# undo button. Also tests if tutorial and save functions work
# WARNING: BuildPaletteTest takes a very long time ~20 minutes

import time

from testflow.lib.case.basecase import QuirkCase
from testflow.lib.utils.installation import install_android_app
from poco.drivers.unity3d import UnityPoco
from poco.exceptions import InvalidOperationException
from pocounit.suite import PocoTestSuite

from airtest.core.api import device as current_device, connect_device
from airtest.core.api import *


#--------------------------------------------------------------------#
#   BASE CASE                                                        #
#--------------------------------------------------------------------#
class BuildMenuCase(QuirkCase):

    def setUp(self):
        self.poco = UnityPoco()
        if exists(Template(self.R('res/img/default.jpg'))):
            self.createAvatar()
            self.poco("quick_menu_button").click()
            self.poco("build").click()
            time.sleep(3)
            self.poco("BuildNewQuirkButton").click()
            time.sleep(10)

    # @classmethod
    # def tearDownClass(cls):
    #     super(QuirkCase, cls).tearDownClass()


#--------------------------------------------------------------------#
#   TEST CASES                                                       #
#--------------------------------------------------------------------#
# Clicks on every single object and tries to place them
class PaletteTest(BuildMenuCase):

    def placeBlock(self, path):
        self.poco("PaletteTab").click()
        self.poco("MultiFlowConfigurationPointerImage").click()
        self.checkHelper(path)
        self.poco("UndoButton").click()
        self.poco("PaletteTab").click()

    def checkHelper(self, path, recapture=True):
        if recapture:
            snapshot('../../' + path)
        with self.subTest(Template=path):
            assert_exists(Template(self.R(path), rgb=True, threshold=0.8),
                          "Failed to find " + path.replace('res/img/buildmenu/', ''))

    def testColors(self, color_grid, block_list, block_name, toggle_name):
        for color in color_grid.children():
            color_name = color.get_name()
            try:
                self.poco("ColorGrid").child(color_name).click()
            except InvalidOperationException:
                self.scrollDownClick(block_list, color_name)
            finally:
                self.checkHelper('res/img/buildmenu/' +
                                 toggle_name + '/' + block_name +
                                 color_name + '.png')

    def helper(self):

        self.poco("PaletteTab").click()

        nav_bar = self.poco("PaletteCategories").offspring("ScrollView")

        for toggle in nav_bar.child("ScrollContent").children():
            toggle_name = toggle.get_name().replace("PaletteTab", "")
            try:
                print("Testing... " + toggle_name)
                self.poco(toggle.get_name()).click()
            except InvalidOperationException:
                print("Scrolling nav bar...")
                self.scrollDownClick(nav_bar, toggle.get_name())
            finally:
                block_list = self.poco(
                    "PaletteBlockGroups").offspring("ScrollView")
                for block in block_list.child("ScrollContent").children():
                    block_name = block.get_name()
                    try:
                        self.poco(block_name).click()
                        color_grid = self.poco(
                            block_name + "Description").child("ColorGrid")
                        if color_grid.exists():
                            self.testColors(
                                color_grid, block_list, block_name, toggle_name)
                            self.scrollUpClick(block_list, block_name)
                    except InvalidOperationException:
                        self.scrollDownClick(block_list, block_name)
                    finally:
                        self.placeBlock('res/img/buildmenu/' +
                                        toggle_name + "/" +
                                        block_name + '.png')

    def runTest(self):
        assert_exists(Template(self.R('res/img/buildscreen.jpg')),
                      "Failed to enter build screen")
        self.helper()

    # to close build palette
    def tearDown(self):
        self.poco("BuildPalette").click()


# Tests if tutorial works and can be navigated
class TutorialTest(BuildMenuCase):

    def runTest(self):
        assert_exists(Template(self.R('res/img/buildscreen.jpg')),
                      "Failed to enter build screen")
        self.poco("TutButton").click()
        snapshot('../../res/img/buildmenu/tutorial.jpg')
        assert_exists(Template(self.R('res/img/buildmenu/tutorial.jpg')),
                      "Tutorial confirm did not show up")
        self.poco("Accept").click()
        time.sleep(5)
        for i in range(2, 5):
            snapshot('../../res/img/buildmenu/tutorial' + str(i) + '.jpg')
            assert_exists(Template(self.R('res/img/buildmenu/tutorial' + str(i) + '.jpg')),
                          "Tutorial screen did not show up")
            self.poco("NextButton").click([0.5, 0.9])
        assert_exists(Template(self.R('res/img/buildscreen.jpg')),
                      "Tutorial did not hide")


# Tests if map can be saved
# Doesn't actually save a map because Poco can't input text, but checks for
# all relevant UI
class SaveTest(BuildMenuCase):

    # tests only preview and save, checks for menu existence
    def runTest(self):
        assert_exists(Template(self.R('res/img/buildscreen.jpg')),
                      "Failed to enter build screen")
        self.poco("MenuButton").click()
        # snapshot('../../res/img/buildmenu/save.jpg')
        assert_exists(Template(self.R('res/img/buildmenu/save.jpg')),
                      "Save menu did not show")
        self.poco("PreviewButton").click()
        self.assertTrue(self.poco("ReturnButton").exists(), "Preview failed")
        self.poco("ReturnButton").click()
        self.poco("MenuButton").click()
        self.poco("SaveButton").click()
        self.assertTrue(self.poco("InputField").exists())
        self.poco("CancelButton").click()
        self.poco("ExitBuildModeButton").click()
        time.sleep(10)
        assert_exists(Template(self.R('res/img/Commons.jpg')),
                      "Failed to return to Commons after exit build mode")

    def tearDown(self):
        self.poco("quick_menu_button").click()
        self.poco("build").click()
        time.sleep(3)
        self.poco("BuildNewQuirkButton").click()
        time.sleep(10)


if __name__ == '__main__':
    import pocounit
    pocounit.main()
