import win32api, win32gui, win32con
from ctypes import *
import time

def getCurPos():
    return win32gui.GetCursorPos()


def getPos():
    while True:
        res = getCurPos()
        print(res)
        time.sleep(1)


def clickLeft():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def movePos(x, y):
    windll.user32.SetCursorPos(x, y)


def animateMove(curPos, targetPos, durTime=1, fps=60):
    x1 = curPos[0]
    y1 = curPos[1]
    x2 = targetPos[0]
    y2 = targetPos[1]
    dx = x2 - x1
    dy = y2 - y1
    times = int(fps * durTime)
    dx_ = dx * 1.0 / times
    dy_ = dy * 1.0 / times
    sleep_time = durTime * 1.0 / times
    for i in range(times):
        int_temp_x = int(round(x1 + (i + 1) * dx_))
        int_temp_y = int(round(y1 + (i + 1) * dy_))
        windll.user32.SetCursorPos(int_temp_x, int_temp_y)
        time.sleep(sleep_time)
    windll.user32.SetCursorPos(x2, y2)


def animateMoveAndClick(curPos, targetPos, durTime=1, fps=60, waitTime=1):
    x1 = curPos[0]
    y1 = curPos[1]
    x2 = targetPos[0]
    y2 = targetPos[1]
    dx = x2 - x1
    dy = y2 - y1
    times = int(fps * durTime)
    dx_ = dx * 1.0 / times
    dy_ = dy * 1.0 / times
    sleep_time = durTime * 1.0 / times

    for i in range(times):
        int_temp_x = int(round(x1 + (i + 1) * dx_))
        int_temp_y = int(round(y1 + (i + 1) * dy_))
        windll.user32.SetCursorPos(int_temp_x, int_temp_y)
        time.sleep(sleep_time)
    windll.user32.SetCursorPos(x2, y2)
    time.sleep(waitTime)
    clickLeft()