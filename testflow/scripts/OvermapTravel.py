# coding=utf-8
__author__ = "Eric"

from testflow.lib.case.basecase import QuirkCase
from poco.drivers.unity3d import UnityPoco
from testflow.lib.case.suite import QuirkSuite

from airtest.core.api import *


class OvermapTravelCase(QuirkCase):

    # pass both setUpClass and tearDownClass when using with a suite
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.poco = UnityPoco()
        self.poco("quick_menu_button").click()
        self.poco("overmap").click()

    def travel(self, location):
        outposts = {"homebase": "hb",
                    "Commons": "c",
                    "Backyard_Brawl": "bb",
                    "Finders_Falls": "ff",
                    "Quirk_Speedway": "qs",
                    "battle": "b",
                    "playground": "pg"}
        touch(
            Template(self.R('res/img/overmap_icons/icon_' + outposts[location] + '.png')))

        time.sleep(3)
        if exists(Template(self.R('res/img/infection.png'))) and location == "playground":
            self.poco("DismissButton").click()
            location = location + "_infection"

        time.sleep(12)
        if self.poco("looking").exists():
            self.poco("looking").click()
            self.poco("quick_play").click()
            self.assertTrue(exists(Template(self.R('res/img/overmap.png'))))
        else:
            # snapshot('../../res/img/outposts/' + location + '.png')
            self.assertTrue(
                exists(Template(self.R('res/img/outposts/' + location + '.png'))))

            if location in ["battle", "playground"]:
                self.poco("ExitButton").click()
                self.poco("Accept").click()
            elif location == "playground_infection":
                self.poco("ExitButtonDisabled").click()
                self.poco("Accept").click()


class Homebase(OvermapTravelCase):

    def runTest(self):
        self.travel("homebase")


class Commons(OvermapTravelCase):

    def runTest(self):
        self.travel("Commons")


class BackyardBrawl(OvermapTravelCase):

    def runTest(self):
        self.travel("Backyard_Brawl")


class FindersFalls(OvermapTravelCase):

    def runTest(self):
        self.travel("Finders_Falls")


class QuirkSpeedway(OvermapTravelCase):

    def runTest(self):
        self.travel("Quirk_Speedway")


class QuickPlayBattle(OvermapTravelCase):

    def runTest(self):
        self.travel("battle")


class QuickPlayPlayground(OvermapTravelCase):

    def runTest(self):
        self.travel("playground")


if __name__ == '__main__':
    suite = QuirkSuite([
        Homebase(),
        Commons(),
        BackyardBrawl(),
        FindersFalls(),
        QuirkSpeedway(),
        QuickPlayPlayground(),
        QuickPlayBattle()
    ])
    import pocounit
    pocounit.run(suite)
