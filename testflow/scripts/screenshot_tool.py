# coding=utf-8

import json
import time
from poco.drivers.unity3d import UnityPoco as Poco
from airtest.core.api import start_app, stop_app, Template, exists, snapshot
from base64 import b64decode

poco = Poco()
path = snapshot('../../res/img/chat/emoji_chat.png')
print("path:" + path)
