import win32api, win32con
from time import sleep

LInterval = 0.045
#RInterval = 0.023

def click(x,y, button = "left"):
    win32api.SetCursorPos((x,y))
    if button == "left":
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        sleep(0.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    elif button == "right":
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
        sleep(0.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)

while True:
    x,y = win32api.GetCursorPos()
    
    if win32api.GetAsyncKeyState(win32con.VK_XBUTTON2) or win32api.GetAsyncKeyState(win32con.VK_XBUTTON1):
        # if win32api.GetAsyncKeyState(win32con.VK_LBUTTON) != 0:
        # print(win32api.GetAsyncKeyState(win32con.VK_XBUTTON2))
        # print(win32api.GetAsyncKeyState(win32con.VK_LBUTTON))
        click(x,y, button = "left")
        sleep(LInterval)
    # if win32api.GetAsyncKeyState(win32con.VK_XBUTTON1):
    #     # print(win32api.GetAsyncKeyState(win32con.VK_XBUTTON2))
    #     # print(win32api.GetAsyncKeyState(win32con.VK_LBUTTON))
    #     click(x,y, button = "right")
    #     sleep(RInterval)
    
    
