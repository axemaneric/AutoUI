# coding=utf-8

from poco.drivers.unity3d import UnityPoco
from airtest.core.api import snapshot

poco = UnityPoco()
path = snapshot('../../res/img/optionsmenu/accountfound.jpg')
print("path:" + path)
