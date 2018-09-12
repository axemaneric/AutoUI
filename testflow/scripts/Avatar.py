# coding=utf-8
__author__ = "Eric"

# Test script for avatar customization accessed through side menu. Since money
# isn't infinite, only checks if item is able to be previewed inside store.

from testflow.lib.case.basecase import QuirkCase
from testflow.lib.case.suite import QuirkSuite
from testflow.lib.utils.installation import install_android_app
from poco.drivers.unity3d import UnityPoco
from poco.exceptions import InvalidOperationException
from pocounit.suite import PocoTestSuite

from airtest.core.api import device as current_device, connect_device
from airtest.core.api import *


class Avatar(QuirkCase):

    def setUp(self):
        self.createAvatar()
        self.poco("quick_menu_button").click()
        self.poco("avatar").click()

    def loopItems(self, name, recapture=True):
        if self.poco("NewGrid").exists():
            content_grid = self.poco("NewGrid")
        else:
            content_grid = self.poco("ContentGrid")
        index = 1
        for item in content_grid.children():
            try:
                item.child("Background").click()
            except InvalidOperationException:
                print('Scrolling...')
                scrollview = self.poco("Viewport")
                scrolls = 0
                while scrolls < 8:
                    try:
                        item.child("Background").click()
                        break
                    except InvalidOperationException:
                        print("Scrolling to find")
                        scrollview.focus([1, 0.8]).drag_to(
                            scrollview.focus([1, 0.2]))
                        time.sleep(1)
                    scrolls += 1
            finally:
                if recapture:
                    snapshot("../../res/img/avatar/" +
                             name + "/" + str(index) + ".jpg")
                self.assertTrue(exists(Template(self.R(
                    "res/img/Avatar/" + name + "/" + str(index) + ".jpg"), rgb=True, threshold=0.9)))
            index += 1

    def runTest(self):
        nav_bar = self.poco("SalonNavbarMobile(Clone)")
        nav_bar_children = self.poco("ToggleGroup").children()
        for toggle in nav_bar_children:
            name = toggle.get_name()
            try:
                print("Testing... " + name)
                self.poco(name).click()
            except InvalidOperationException:
                print("Scrolling nav bar...")
                nav_bar.focus([0.5, 0.8]).drag_to(
                    nav_bar.focus([0.5, 0.2]))
                self.poco(name).click()
            finally:
                if name == "ColorToggle":
                    self.loopItems(name + "/SkinToggle")
                    self.poco("HairToggle").click()
                    print('Scrolling...')
                    scrollview = self.poco("Viewport")
                    scrollview.focus([0.5, 0.2]).drag_to(
                        scrollview.focus([0.5, 0.8]))
                    self.loopItems(name + "/HairToggle")
                else:
                    self.loopItems(name)

    def tearDown(self):
        self.poco("DismissButton").click()


if __name__ == '__main__':
    import pocounit
    pocounit.main()
