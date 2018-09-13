# coding=utf-8

from testflow.lib.case.basecase import QuirkCase
from pocounit.suite import PocoTestSuite
from testflow.lib.utils.installation import *

from airtest.core.api import device as current_device, connect_device
from airtest.core.api import *


class QuirkSuite(PocoTestSuite, QuirkCase):

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
