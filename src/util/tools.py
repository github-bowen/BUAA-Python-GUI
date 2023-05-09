# -*- coding = utf-8 -*-
# @Time :2022/8/2 13:59
# @Author:banana889
# @File : tools.py
DEBUG_ = False
def debugPrint(s : str):
    if(DEBUG_):
        print("\033[34m" + s + "\033[0m")

def debugWarning(s : str):
    if (DEBUG_):
        print("\033[35m" + s + "\033[0m")

# debugWarning("a")