# coding=utf-8
__author__ = "Eric"

# Test script for Emoji function in left of Quirk HUD.

import time

from testflow.lib.case.basecase import QuirkCase
from poco.exceptions import PocoNoSuchNodeException

from airtest.core.api import *


class Emoji(QuirkCase):

    @classmethod
    def setUpClass(cls):
        super(EmojiCase, cls).setUpClass()
        cls.installQuirk()
        cls.createAvatar()

    def setUp(self):
        self.poco("pop_out_button").click()

    def quickEmoteTest(self):
        if exists(Template(self.R('res/img/emoji/more.jpg'))):
            self.poco("pop_out_button").click()
        self.assertTrue(self.poco("quick_list").exists())
        quick_emoji_list = self.poco("quick_list").offspring(
            "recent_content").children()
        index = 0
        for emoji in quick_emoji_list:
            emoji.click()
            snapshot('../../res/img/emoji/quick' + str(index) + '.jpg')
            self.check(Template(self.R('res/img/emoji/quick' + str(index) + '.jpg')), "Quick " + str(index) + " not found on screen")
            index += 1

    def fullEmoteTest(self):
        if not exists(Template(self.R('res/img/emoji/more.jpg'))):
            self.poco("more").click()
        self.assertTrue(exists(Template(self.R('res/img/emoji/more.jpg'))), "Full emote menu not found")
        categories = self.poco("categories").children()
        for category in categories:
            category.click()
            cat_name = category.get_name().replace("_tab_", "_")
            snapshot('../../res/img/emoji/' + cat_name + '.jpg')
            self.check(Template(self.R('res/img/emoji/' + cat_name + '.jpg')), cat_name + " Category not found")
            content_list = self.poco(cat_name).children()
            index = 0
            for item in content_list:
                item.click()
                snapshot('../../res/img/emoji/' + cat_name + str(index) + '.jpg')
                self.check(Template(self.R('res/img/emoji/' + cat_name + str(index) + '.jpg')), cat_name + str(index) + ' item not found')
                if cat_name.startswith("emotes"):
                    time.sleep(5)
                index += 1

    def runTest(self):
        self.quickEmoteTest()
        self.fullEmoteTest()

    def tearDown(self):
        self.poco("pop_out_button").click()


if __name__ == '__main__':
    import pocounit
    pocounit.main()
