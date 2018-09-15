# coding=utf-8
__author__ = "Eric"

# Test script for side Menu Bar. Checks if every one of them as accessible and
# directs character to the correct scene. Contains individual tests and
# a full test.

from testflow.lib.case.basecase import QuirkCase
from poco.drivers.unity3d import UnityPoco
from testflow.lib.case.suite import QuirkSuite

from airtest.core.api import *


#--------------------------------------------------------------------#
#   BASE CASE                                                        #
#--------------------------------------------------------------------#
# contains all tests, but class object must be created to use the methods with
# inheritence
class MenuBarCase(QuirkCase):

    def setUp(self):
        self.poco = UnityPoco()
        # self.createAvatar()
        self.poco("quick_menu_button").click()

    # @classmethod
    # def tearDownClass(cls):
    #     pass

    def testOvermap(self):
        self.poco("overmap").click()
        # snapshot('../../res/img/overmap.jpg')
        with self.subTest(test="overmap"):
            assert_exists(Template(self.R('res/img/overmap.jpg')),
                          "Failed to enter overmap")
        close_btn = self.poco("OvermapCloseButton")
        if close_btn.exists():
            close_btn.click()

    def testHomebase(self):
        self.poco("home_base").click()
        time.sleep(15)
        # snapshot('../../res/img/homebase.jpg')
        with self.subTest(test="Homebase"):
            assert_exists(Template(self.R('res/img/homebase.jpg')),
                          "Failed to enter homebase")
        menu_btn = self.poco("quick_menu_button")
        if menu_btn.exists():
            menu_btn.click()
            self.poco("return_to_outpost").click()

    def testQuickPlay(self):
        self.poco("quick_play").click()
        # snapshot('../../res/img/quick_play.jpg')
        with self.subTest(test="quickplay"):
            assert_exists(Template(self.R('res/img/quick_play.jpg')),
                          "Failed to enter quick play screen")
        close_btn = self.poco("CloseButton")
        if close_btn.exists():
            close_btn.click()

    def testTinkering(self):
        self.poco("tinkering").click()
        time.sleep(5)
        # snapshot('../../res/img/tinkering.jpg')
        with self.subTest(test="tinkering"):
            assert_exists(Template(self.R('res/img/tinkering.jpg')),
                          "Failed to enter tinkering screen")
        self.poco("ExitButton").click()

    def testAvatar(self):
        self.poco("avatar").click()
        time.sleep(5)
        # snapshot('../../res/img/avatar.jpg')
        with self.subTest(test="Avatar"):
            assert_exists(Template(self.R('res/img/avatar.jpg')),
                          "Failed to enter avatar customization")
        self.poco("DismissButton").click()

    def testBuild(self):
        self.poco("build").click()
        time.sleep(3)
        with self.subTest(test="build"):
            assert_exists(Template(self.R('res/img/build.jpg')),
                          "Failed to enter build menu")
        self.poco("CloseButton").click()

    def testGizmos(self):
        self.poco("gizmos").click()
        time.sleep(15)
        # snapshot('../../res/img/gizmos.jpg')
        with self.subTest(test="gizmos"):
            assert_exists(Template(self.R('res/img/gizmos.jpg')),
                          "Failed to enter Gizmos building")
        self.poco("ExitMatch").click()
        self.poco("Accept").click()

    def testOptions(self):
        self.poco("options").click()
        with self.subTest(test="options"):
            assert_exists(Template(self.R('res/img/options.jpg')),
                          "Failed to enter options menu")
        self.poco("exit_container").click()


#--------------------------------------------------------------------#
#   TEST CASES                                                       #
#--------------------------------------------------------------------#
# class Overmap(MenuBarCase):

#     def runTest(self):
#         self.testOvermap()


# class MenuHomebase(MenuBarCase):

#     def runTest(self):
#         self.testHomebase()


# class QuickPlay(MenuBarCase):

#     def runTest(self):
#         self.testQuickPlay()


# class Avatar(MenuBarCase):

#     def runTest(self):
#         self.testAvatar()


# class Tinkering(MenuBarCase):

#     def runTest(self):
#         self.testTinkering()


# class Build(MenuBarCase):

#     def runTest(self):
#         self.testBuild()


# class Gizmos(MenuBarCase):

#     def runTest(self):
#         self.testGizmos()


# class Options(MenuBarCase):

#     def runTest(self):
#         self.testOptions()


class AllIcons(MenuBarCase):

    def runTest(self):
        self.testOvermap()
        self.poco("quick_menu_button").click()
        self.testHomebase()
        time.sleep(15)
        self.poco("quick_menu_button").click()
        self.testQuickPlay()
        self.poco("quick_menu_button").click()
        self.testAvatar()
        time.sleep(10)
        self.poco("quick_menu_button").click()
        self.testTinkering()
        time.sleep(10)
        self.poco("quick_menu_button").click()
        self.testBuild()
        self.poco("quick_menu_button").click()
        self.testGizmos()
        time.sleep(10)
        self.poco("quick_menu_button").click()
        self.testOptions()


if __name__ == '__main__':
    import pocounit
    pocounit.main()
