# coding=utf-8
__author__ = "Eric"

import time

from testflow.lib.case.unity_game import QuirkCase
from testflow.lib.utils.installation import install_android_app
from poco.drivers.unity3d import UnityPoco
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from poco.exceptions import InvalidOperationException
from pocounit.suite import PocoTestSuite

from airtest.core.api import device as current_device, connect_device
from airtest.core.api import *


class Chat(QuirkCase):

    @classmethod
    def setUpClass(cls):
        super(Chat, cls).setUpClass()
        cls.createAvatar()

    def runTest(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == '__main__':
    import pocounit
    pocounit.main()
