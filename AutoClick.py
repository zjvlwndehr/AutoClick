import win32api, win32con
from time import sleep

interval = 0.085

def click(x,y, button = "left"):
    win32api.SetCursorPos((x,y))
    if button == "left":
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    elif button == "right":
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)

while True:
    x,y = win32api.GetCursorPos()
    # if button is pressed
    if win32api.GetAsyncKeyState(win32con.VK_XBUTTON2) != 0 and win32api.GetAsyncKeyState(win32con.VK_LBUTTON) != 0:
        print("L")
        click(x,y, button = "left")
        sleep(interval)
    if win32api.GetAsyncKeyState(win32con.VK_XBUTTON2) != 0 and win32api.GetAsyncKeyState(win32con.VK_RBUTTON) != 0:
        print("R")
        click(x,y, button = "right")
        sleep(interval)
