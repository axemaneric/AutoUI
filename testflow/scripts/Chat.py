# coding=utf-8
__author__ = "Eric"

import time

from testflow.lib.case.unity_game import QuirkCase
from testflow.lib.utils.installation import *
from poco.drivers.unity3d import UnityPoco
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from poco.exceptions import InvalidOperationException
from pocounit.suite import PocoTestSuite

from airtest.core.api import device as current_device, connect_device
from airtest.core.api import *


class ChatCase(QuirkCase):

    @classmethod
    def setUpClass(cls):
        super(ChatCase, cls).setUpClass()
        cls.createAvatar()

    def setUp(self):
        self.poco = UnityPoco()
        self.poco("quick_menu_button").click()
        self.poco("return_to_outpost").click()
        time.sleep(10)
        self.assertTrue(
            exists(Template(self.R('res/img/chat/Commons.png'))), "Not in Commons")
        self.poco("widget_toggle").click()
        self.assertTrue(exists(Template(self.R(
            'res/img/optionsmenu/age_verify.png'))), "Age verification screen not found")

    @classmethod
    def tearDownClass(cls):
        stop_app(cls.package_name)
        uninstall(cls.package_name)


# BEGIN: Age Verify -> Help screen -> Select over 13 then under 13 -> Parent
# consent screen -> Click "NOT NOW" -> Parent Availability Screen -> Back to
# parent consent screen -> Click "I AM A PARENT" -> Email Screen -> Click
# "SEND EMAIL" -> Invalid Email Appears -> Click "NOT NOW" -> In Parent
# Availability screen click "OKAY" -> Exit to Commons: END
class ChatYoung(ChatCase):

    def runTest(self):
        self.poco("help").click()
        self.assertTrue(exists(
            Template(self.R('res/img/optionsmenu/age_help.png'))),
            "Help screen not found")
        self.poco("back").click()
        self.poco("of_age").click()
        self.poco("too_young").click()
        self.poco("continue").click()
        self.assertTrue(exists(Template(self.R('res/img/optionsmenu/parental_consent.png'))),
                        "Parent consent sreen not found")
        self.poco("not_now").click()
        self.assertTrue(exists(Template(self.R(
            'res/img/optionsmenu/parent_unavailable.png'))),
            "Parent availability screen not found")
        self.poco("back").click()
        self.poco("i_am_a_parent").click()
        self.assertTrue(exists(Template(self.R('res/img/optionsmenu/parent_verification.png'))),
                        "Parent verification screen not found")
        self.poco("send_email").click()
        self.assertTrue(exists(Template(self.R('res/img/chat/email_invalid.png'))),
                        "Email invalid did not show up")
        self.poco("not_now").click()
        self.poco("okay").click()
        self.assertTrue(exists(Template(self.R('res/img/Commons.png'))),
                        "Not in Commons after age verification (young)")


# Simple test to test for both age verification and sending emojis
# BEGIN: Age Verify Screen -> Select over 13 and continue -> Check for chat
# screen -> Input all four emojis -> Send -> Check if message sent in chat: END
class EmojiChat(ChatCase):

    def runTest(self):
        self.poco("of_age").click()
        self.poco("continue").click()
        self.assertTrue(exists(Template(self.R('res/img/chat/chat.png'))),
                        "Chat screen not found")
        self.poco("emoji").click()
        for emoji in self.poco("chat_container").children():
            emoji.click()
            self.poco("emoji").click()
        self.poco("emoji").click()
        self.poco("send").click()
        snapshot('../../res/img/chat/emoji_chat.png')
        self.assertTrue(exists(Template(self.R('res/img/chat/emoji_chat.png'))),
                        "Chat with emoji not found on screen")


if __name__ == '__main__':
    import pocounit
    pocounit.main()
