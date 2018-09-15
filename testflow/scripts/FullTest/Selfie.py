# coding=utf-8
__author__ = "Eric"

# Test script for Selfie feature in top bar. Tests all frames, takes a selfie,
# retakes, and share selfie feature.

import time

from testflow.lib.case.basecaseNoUninstall import QuirkCase
from poco.drivers.unity3d import UnityPoco
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

from airtest.core.api import *


class Selfie(QuirkCase):

    def setUp(self):
        self.poco = UnityPoco()
        # snapshot('../../res/img/Commons.jpg')
        self.poco("camera").click()

    # Used for allowing access to access android files
    # Only needs to be executed once
    def allowFileAccess(self):
        # snapshot('../../res/img/selfie/allow_save.jpg')
        self.poco = AndroidUiautomationPoco(screenshot_each_action=False)
        self.poco("com.android.packageinstaller:id/permission_allow_button").click()
        # snapshot('../../res/img/selfie/saved.jpg')
        assert_exists(Template(self.R('res/img/selfie/saved.jpg')),
                      "Picture saved screen not found on screen")
        self.poco = UnityPoco()

    def cameraTrigger(self):
        if self.poco("camera").exists():
            self.poco("camera").click()
        self.poco("take_photo").click()
        assert_exists(Template(self.R('res/img/selfie/frame.jpg')),
                      "Frame selection screen not found")

    def exitCamera(self, need_confirm=True):
        current_state = snapshot('../../res/img/selfie/temp.jpg')
        self.poco("exit_container").click()
        if need_confirm:
            assert_exists(Template(self.R('res/img/selfie/exit_confirm.jpg')),
                          "No exit confirmation screen showed up")
            self.poco("cancel").click()
            assert_exists(Template(current_state))
            self.poco("exit_container").click()
            self.poco("exit_camera").click()
        assert_exists(Template(self.R('res/img/Commons.jpg')),
                      "Failed to return to Commons after exit camera")

    def zoomTest(self):
        self.poco("handle").drag_to(self.poco("zoom_slider").focus([0.5, 0]))
        # snapshot('../../res/img/selfie/100.jpg')
        assert_exists(Template(self.R('res/img/selfie/100.jpg')),
                      "Failed to zoom in 100%")
        self.poco("handle").drag_to(self.poco("zoom_slider").focus([0.5, 1]))
        # snapshot('../../res/img/selfie/0.jpg')
        assert_exists(Template(self.R('res/img/selfie/0.jpg')),
                      "Failed to zoom out 0%")

    def emoteTest(self):
        emotes = self.poco("emotes_container").children()
        for emote in emotes:
            emote.click()
            # snapshot('../../res/img/selfie/' + emote.get_name() + '.jpg')
            assert_exists(Template(self.R('res/img/selfie/' + emote.get_name() +
                                          '.jpg')), "Emote: " + emote.get_name() + " not used")
            time.sleep(5)

    def reverseTest(self):
        self.poco("toggle").click()
        # snapshot('../../res/img/selfie/scenic.jpg')
        assert_exists(Template(self.R('res/img/selfie/scenic.jpg')),
                      "Failed to scenic mode")
        self.poco("toggle").click()
        assert_exists(Template(self.R('res/img/selfie/menu.jpg')),
                      "Failed to switch to selfie mode")

    def retakeTest(self):
        self.cameraTrigger()
        self.poco("retake").click()
        assert_exists(Template(self.R('res/img/selfie/menu.jpg')),
                      "Retake button did not take user back to camera mode")
        self.exitCamera(need_confirm=False)

    # shareTest only tests if Facebook option works
    # Exits to Commons
    # shareTest needs to be manually tested if disabled in alpha environment
    # if not disabled, shareTest needs to be updated once other sharing options
    # are implemented
    def shareTest(self, file_access=False):
        self.cameraTrigger()
        self.poco("continue").click()
        self.poco("save_and_share").click()
        # snapshot('../../res/img/selfie/share.jpg')
        assert_exists(Template(self.R('res/img/selfie/share.jpg')),
                      "Share tab did not pop out")
        for button in self.poco("share_panel").offspring("container").children():
            button.click()
            time.sleep(5)
            if button.get_name() == "facebook":
                if not file_access:
                    self.allowFileAccess()
                assert_exists(Template(self.R('res/img/selfie/frame.jpg')),
                              "Did not go back to frame selection")
                self.poco("continue").click()
                self.poco("save_and_share").click()
        self.poco("exit").click()
        assert_not_exists(Template(
            self.R('res/img/selfie/share.jpg'), threshold=0.9), "Share tab did not hide")
        self.exitCamera(need_confirm=True)

    def frameTest(self):
        self.cameraTrigger()
        scrollview = self.poco("frame_scroll_view")
        for frame in self.poco("content").children():
            frame_name = frame.get_name()
            # snapshot('../../res/img/selfie/frames/' + frame_name + '.jpg')
            with self.subTest(frame=frame_name):
                assert_exists(
                    Template(self.R('res/img/selfie/frames/' + frame_name + '.jpg')))
            scrollview.focus([1, 0.5]).drag_to(scrollview.focus([0, 0.5]))
            time.sleep(2)
        self.exitCamera(need_confirm=True)
        # self.retakeTest()

    # Android files are allowed access after execution
    def takeSelfieTest(self, file_access=False):
        # snapshot('../../res/img/selfie/menu.jpg')
        self.cameraTrigger()
        # snapshot('../../res/img/selfie/frame.jpg')
        assert_exists(Template(self.R('res/img/selfie/frame.jpg')),
                      "Frame selection screen not found")
        self.poco("continue").click()
        # snapshot('../../res/img/selfie/save.jpg')
        assert_exists(
            Template(self.R('res/img/selfie/save.jpg')), "Save Photo screen not found")
        self.poco("continue").click()
        print("Switching to native Poco")
        time.sleep(5)
        if not file_access:
            self.allowFileAccess()
        time.sleep(5)
        self.poco("picture_saved_container").child("continue").click()
        time.sleep(1)
        assert_exists(Template(self.R('res/img/selfie/menu.jpg')),
                      "Selfie screen not found after picture taken")

    def runTest(self):
        assert_exists(Template(self.R('res/img/selfie/menu.jpg')),
                      "Failed to load into camera")
        self.zoomTest()
        self.emoteTest()
        self.reverseTest()
        self.takeSelfieTest()
        self.frameTest()
        self.shareTest(file_access=True)
        self.retakeTest()


if __name__ == '__main__':
    import pocounit
    pocounit.main()
