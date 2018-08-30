# coding=utf-8
__author__ = "Eric"

from testflow.lib.case.unity_game import QuirkCase
from poco.drivers.unity3d import UnityPoco
from testflow.lib.case.suite import QuirkSuite

from airtest.core.api import *


class MenuBarCase(QuirkCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.maxDiff = None
        self.assertErrors = []
        self.poco = UnityPoco()
        self.poco("quick_menu_button").click()

    def tearDown(self):
        self.assertEqual([], self.assertErrors)

    @classmethod
    def tearDownClass(cls):
        pass

    def testOvermap(self):
        self.poco("overmap").click()
        # snapshot('../../res/img/overmap.png')
        self.check(Template(self.R('res/img/overmap.png')),
                   "Failed to enter overmap")
        close_btn = self.poco("OvermapCloseButton")
        if close_btn.exists():
            close_btn.click()

    def testHomebase(self):
        self.poco("home_base").click()
        time.sleep(10)
        snapshot('../../res/img/homebase.png')
        self.check(Template(self.R('res/img/homebase.png')),
                   "Failed to enter homebase")
        menu_btn = self.poco("quick_menu_button")
        if menu_btn.exists():
            menu_btn.click()
            self.poco("return_to_outpost").click()

    def testQuickPlay(self):
        self.poco("quick_play").click()
        # snapshot('../../res/img/quick_play.png')
        self.check(Template(self.R('res/img/quick_play.png')),
                   "Failed to enter quick play screen")
        close_btn = self.poco("CloseButton")
        if close_btn.exists():
            close_btn.click()

    def testTinkering(self):
        self.poco("tinkering").click()
        time.sleep(5)
        # snapshot('../../res/img/tinkering.png')
        self.check(Template(self.R('res/img/tinkering.png')),
                   "Failed to enter tinkering screen")
        self.poco("ExitButton").click()

    def testAvatar(self):
        self.poco("avatar").click()
        time.sleep(5)
        # snapshot('../../res/img/avatar.png')
        self.check(Template(self.R('res/img/avatar.png')),
                   "Failed to enter avatar customization")
        self.poco("DismissButton").click()

    def testBuild(self):
        self.poco("build").click()
        time.sleep(3)
        self.check(Template(self.R('res/img/build.png')),
                   "Failed to enter build menu")
        self.poco("CloseButton").click()

    def testGizmos(self):
        self.poco("gizmos").click()
        time.sleep(10)
        # snapshot('../../res/img/gizmos.png')
        self.check(Template(self.R('res/img/gizmos.png')),
                   "Failed to enter Gizmos building")
        self.poco("ExitMatch").click()
        self.poco("Accept").click()

    def testOptions(self):
        self.poco("options").click()
        self.check(Template(self.R('res/img/options.png')),
                   "Failed to enter options menu")
        self.poco("exit_container").click()


class Overmap(MenuBarCase):

    def runTest(self):
        self.testOvermap()


class MenuHomebase(MenuBarCase):

    def runTest(self):
        self.testHomebase()


class QuickPlay(MenuBarCase):

    def runTest(self):
        self.testQuickPlay()


class Avatar(MenuBarCase):

    def runTest(self):
        self.testAvatar()


class Tinkering(MenuBarCase):

    def runTest(self):
        self.testTinkering()


class Build(MenuBarCase):

    def runTest(self):
        self.testBuild()


class Gizmos(MenuBarCase):

    def runTest(self):
        self.testGizmos()


class Options(MenuBarCase):

    def runTest(self):
        self.testOptions()


class FullTest(MenuBarCase):

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
