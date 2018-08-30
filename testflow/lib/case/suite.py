# coding=utf-8

from testflow.lib.case.unity_game import QuirkCase
from pocounit.addons.poco.action_tracking import ActionTracker
from pocounit.addons.poco.capturing import SiteCaptor
from pocounit.suite import PocoTestSuite
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from poco.drivers.unity3d import UnityPoco
from testflow.lib.utils.installation import *
from poco.exceptions import InvalidOperationException


from airtest.core.api import device as current_device, connect_device
from airtest.core.api import *
from airtest.core.helper import device_platform


class QuirkSuite(PocoTestSuite, QuirkCase):

    def setUp(self):
        if not current_device():
            connect_device('Android:///')

        self.package_name = 'com.ugen.playquirk'
        apk_path = self.R('res/app/quirk.apk')
        install_android_app(current_device().adb, apk_path)
        start_app(self.package_name)
        time.sleep(30)

        self.createAvatar()

    def tearDown(self):
        stop_app(self.package_name)
        uninstall(self.package_name)
