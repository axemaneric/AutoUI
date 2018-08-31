# coding=utf-8

from pocounit.case import PocoTestCase
from pocounit.addons.poco.action_tracking import ActionTracker
from pocounit.addons.poco.capturing import SiteCaptor
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from poco.drivers.unity3d import UnityPoco
from testflow.lib.utils.installation import *
from poco.exceptions import InvalidOperationException


from airtest.core.api import device as current_device, connect_device
from airtest.core.api import *
from airtest.core.helper import device_platform


class QuirkCase(PocoTestCase):

    def scrollDownClick(self, scrollview, target, timeout=8):
        scrolls = 0
        while scrolls < timeout:
            try:
                self.poco(target).click()
                return
            except InvalidOperationException:
                print("Scrolling to find: " + target)
                scrollview.focus([1, 0.8]).drag_to(
                    scrollview.focus([1, 0.2]))
                time.sleep(1)
            scrolls += 1
        raise TimeoutError("Target: " + target + " Not Found")

    def scrollUpClick(self, scrollview, target, timeout=8):
        scrolls = 0
        while scrolls < timeout:
            try:
                self.poco(target).click()
                return
            except InvalidOperationException:
                print("Scrolling to find: " + target)
                scrollview.focus([0.5, 0.2]).drag_to(
                    scrollview.focus([0.5, 0.8]))
                time.sleep(1)
            scrolls += 1
        raise TimeoutError("Target: " + target + " Not Found")

    # Catches assertion errors and stores them in a list
    # template: an image Template used to assert existence with
    # msg: failure message at the point of assertion
    def check(self, template, msg=None):
        try:
            self.assertTrue(exists(template), msg)
        except AssertionError as e:
            self.assertErrors.append(str(e))
            return False
        return True

    def createAvatar(self):
        self.maxDiff = None
        self.assertErrors = []
        self.poco = UnityPoco()
        wait(Template(self.R('res/img/default.png')))
        self.poco("SaveButton").click()
        time.sleep(1)
        self.poco("CreateAccountButton").click()
        time.sleep(15)
        overmap_close = self.poco("OvermapCloseButton")
        if overmap_close.exists():
            overmap_close.click()
        time.sleep(5)
        # self.poco("ActionButton").click()
        # time.sleep(5)
        # if exists(Template(self.R('res/img/overmap.png'))):
        #     touch(Template(self.R('res/img/overmap_icons/icon_c.png')))
        # wait(Template(cls.R("res/img/Commons.png")))

    @classmethod
    def createAvatar(cls):
        cls.maxDiff = None
        cls.assertErrors = []
        cls.poco = UnityPoco()
        time.sleep(10)
        cls.poco("SaveButton").click()
        time.sleep(1)
        cls.poco("CreateAccountButton").click()
        time.sleep(15)
        overmap_close = cls.poco("OvermapCloseButton")
        if overmap_close.exists():
            overmap_close.click()
        time.sleep(5)
        # cls.poco("ActionButton").click()
        # time.sleep(5)
        # if exists(Template(cls.R('res/img/overmap.png'))):
        #     touch(Template(cls.R('res/img/overmap_icons/icon_c.png')))
        # wait(Template(cls.R("res/img/Commons.png")))

    @classmethod
    def setUpClass(cls):
        super(QuirkCase, cls).setUpClass()
        if not current_device():
            connect_device('Android:///')

        dev = current_device()
        meta_info_emitter = cls.get_result_emitter('metaInfo')
        if device_platform() == 'Android':
            meta_info_emitter.snapshot_device_info(
                dev.serialno, dev.adb.get_device_info())

        cls.poco = AndroidUiautomationPoco(screenshot_each_action=False)

        action_tracker = ActionTracker(cls.poco)
        cls.register_addon(action_tracker)
        cls.site_capturer = SiteCaptor(cls.poco)
        cls.register_addon(cls.site_capturer)

    @classmethod
    def installQuirk(cls):
        cls.package_name = 'com.ugen.playquirk'
        apk_path = cls.R('res/app/quirk.apk')
        install_android_app(current_device().adb, apk_path)
        start_app(cls.package_name)
        time.sleep(30)

    @classmethod
    def tearDownClass(cls):
        super(QuirkCase, cls).tearDownClass()
        stop_app(cls.package_name)
        uninstall(cls.package_name)
