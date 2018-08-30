# coding=utf-8
__author__ = "Eric"

import time

from testflow.lib.case.basecase import QuirkCase
from testflow.lib.utils.installation import install_android_app
from poco.drivers.unity3d import UnityPoco
from poco.exceptions import InvalidOperationException
from pocounit.suite import PocoTestSuite

from airtest.core.api import device as current_device, connect_device
from airtest.core.api import *


class BuildMenuCase(QuirkCase):

    def placeBlock(self, path):
        self.poco("PaletteTab").click()
        self.poco("MultiFlowConfigurationPointerImage").click()
        self.checkHelper(path)
        self.poco("UndoButton").click()
        self.poco("PaletteTab").click()

    def checkHelper(self, path, recapture=True):
        if recapture:
            snapshot('../../' + path)
        self.check(Template(self.R(path), rgb=True, threshold=0.8),
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
        self.poco("quick_menu_button").click()
        self.poco("build").click()
        time.sleep(3)
        self.poco("BuildNewQuirkButton").click()
        time.sleep(10)
        self.assertTrue(exists(Template(self.R('res/img/buildscreen.png'))),
                        "Failed to enter build screen")
        self.helper()

    def tearDown(self):
        stop_app(self.package_name)
        uninstall(self.package_name)
        self.assertEqual([], self.assertErrors)


if __name__ == '__main__':
    import pocounit
    pocounit.main()
