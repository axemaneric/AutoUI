# coding=utf-8
__author__ = "Eric"

# Test script for Chat feature in Commons. Mainly tests if buttons correctly
# navigate player through various chat verification screens. Refer to testflows
# above ChatYoung and EmojiChat
# ChatYoung tests if parent verification feature
# EmojiChat tests if chat box works by sending emojis
# NOTE: Some test Templates are located in optionsmenu folder

import time

from testflow.lib.case.basecaseNoUninstall import QuirkCase
from testflow.lib.utils.installation import *
from poco.drivers.unity3d import UnityPoco

from airtest.core.api import *


class ChatCase(QuirkCase):

    def setUp(self):
        self.poco = UnityPoco()
        self.poco("widget_toggle").click()


# BEGIN: Age Verify -> Help screen -> Select over 13 then under 13 -> Parent
# consent screen -> Click "NOT NOW" -> Parent Availability Screen -> Back to
# parent consent screen -> Click "I AM A PARENT" -> Email Screen -> Click
# "SEND EMAIL" -> Invalid Email Appears -> Click "NOT NOW" -> In Parent
# Availability screen click "OKAY" -> Exit to Commons: END
class ChatYoung(ChatCase):

    def runTest(self):
        self.assertTrue(exists(Template(self.R(
            'res/img/optionsmenu/age_verify.jpg'))), "Age verification screen not found")
        self.poco("help").click()
        self.assertTrue(exists(
            Template(self.R('res/img/optionsmenu/age_help.jpg'))),
            "Help screen not found")
        self.poco("back").click()
        self.poco("of_age").click()
        self.poco("too_young").click()
        self.poco("continue").click()
        self.assertTrue(exists(Template(self.R('res/img/optionsmenu/parental_consent.jpg'))),
                        "Parent consent sreen not found")
        self.poco("not_now").click()
        self.assertTrue(exists(Template(self.R(
            'res/img/optionsmenu/parent_unavailable.jpg'))),
            "Parent availability screen not found")
        self.poco("back").click()
        self.poco("i_am_a_parent").click()
        self.assertTrue(exists(Template(self.R('res/img/optionsmenu/parent_verification.jpg'))),
                        "Parent verification screen not found")
        self.poco("send_email").click()
        self.assertTrue(exists(Template(self.R('res/img/chat/email_invalid.jpg'))),
                        "Email invalid did not show up")
        self.poco("not_now").click()
        self.poco("okay").click()
        self.assertTrue(exists(Template(self.R('res/img/Commons.jpg'))),
                        "Not in Commons after age verification (young)")


# Simple test to test for both age verification and sending emojis
# BEGIN: Age Verify Screen -> Select over 13 and continue -> Check for chat
# screen -> Input all four emojis -> Send -> Check if message sent in chat: END
class EmojiChat(ChatCase):

    def runTest(self):
        self.poco("of_age").click()
        self.poco("continue").click()
        self.assertTrue(exists(Template(self.R('res/img/chat/chat.jpg'))),
                        "Chat screen not found")
        self.poco("emoji").click()
        for emoji in self.poco("chat_container").children():
            emoji.click()
            self.poco("emoji").click()
        self.poco("emoji").click()
        self.poco("send").click()
        snapshot('../../res/img/chat/emoji_chat.jpg')
        self.assertTrue(exists(Template(self.R('res/img/chat/emoji_chat.jpg'))),
                        "Chat with emoji not found on screen")

    def tearDown(self):
        self.poco("exit_container").click()


if __name__ == '__main__':
    import pocounit
    pocounit.main()
