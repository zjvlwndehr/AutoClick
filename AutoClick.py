import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication

import win32api, win32con, win32gui
import time
from time import sleep

from multiprocessing import Process

class Mouse:
    def __init__(self) -> None:
        self.right_key_bind = 'X1BUTTON'
        self.left_key_bind = 'X2BUTTON'
        self.LInterval = 0.045
        self.RInterval = 0.023
        self.use_right_click = False
        self.Trig = False

    def click(self, x,y, button = "left"):
        win32api.SetCursorPos((x,y))
        if button == "left":
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
            sleep(0.01)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
        elif button == "right":
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
            sleep(0.01)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)

    def proc(self):
        while self.Trig:
            if self.use_right_click == True:
                x,y = win32api.GetCursorPos()
                if win32api.GetAsyncKeyState(win32con.VK_XBUTTON2):
                    self.click(x,y, button = "left")
                    sleep(self.LInterval)
                if win32api.GetAsyncKeyState(win32con.VK_XBUTTON1):
                    self.click(x,y, button = "right")
                    sleep(self.RInterval)
            elif self.use_right_click == False:
                if win32api.GetAsyncKeyState(win32con.VK_XBUTTON2) or win32api.GetAsyncKeyState(win32con.VK_XBUTTON1):
                    x,y = win32api.GetCursorPos()
                    self.click(x,y, button = "left")
                    sleep(self.LInterval)

class APP(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.mouse = Mouse()
        self.pause_or_start_Btn = QPushButton("", self)
        self.pause_or_start_Btn.setText("Go")
        self.UseRclickLabel = QLabel("Use Right click", self)
        self.UseRclickCheckBox = QCheckBox(self)
        self.RightKeyBindingLabel = QLabel("Right click key bind", self)
        self.RightKeyBindingLabel.setText(self.RightKeyBindingLabel.text() + "\t: " + self.mouse.right_key_bind)
        self.LeftKeyBindingLabel = QLabel("Left click key bind", self)
        self.LeftKeyBindingLabel.setText(self.LeftKeyBindingLabel.text() + "\t: " + self.mouse.left_key_bind)
        self.p = Process(target=self.mouse.proc)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Just a tool")
        self.setWindowIcon(QIcon('ico.jpg'))
        self.statusBar().showMessage("Pause")
      
        w = 300
        h = 200

        self.setGeometry(300, 300, w, h)
        
        self.pause_or_start_Btn.setToolTip("Pause the application")
        self.pause_or_start_Btn.setGeometry(int((w-100)/2)+70, int((h-50)/2), 100, 50)
        self.pause_or_start_Btn.clicked.connect(self.pause_or_start)

        self.UseRclickLabel.setGeometry(10, 50, 100, 20)
        self.UseRclickCheckBox.setGeometry(100, 50, 20, 20)
        self.UseRclickCheckBox.stateChanged.connect(self.UseRclickCheckBoxChanged)

        self.RightKeyBindingLabel.setGeometry(10, 80, 200, 40)
        self.LeftKeyBindingLabel.setGeometry(10, 100, 200, 40)


        exitAction = QAction(QIcon('exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')

        exitAction.triggered.connect(qApp.quit)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)

        self.show()

    def UseRclickCheckBoxChanged(self):
        if self.UseRclickCheckBox.isChecked():
            self.mouse.use_right_click = True
            self.RightKeyBindingLabel.setText("Right click key bind" + "\t: " + "X1BUTTON")
            self.LeftKeyBindingLabel.setText("Left click key bind" + "\t: " + "X2BUTTON")
        else:
            self.mouse.use_right_click = False
            self.RightKeyBindingLabel.setText("Right click key bind" + "\t: " + "None")
            self.LeftKeyBindingLabel.setText("Left click key bind" + "\t: " + "X1BUTTON\n" + "X2BUTTON")
    
    def pause_or_start(self):
        if self.statusBar().currentMessage() == "Pause":
            self.mouse.Trig = True
            self.p.start()
            self.statusBar().showMessage("Running...")
            self.pause_or_start_Btn.setText("Pause")
        else:
            self.mouse.Trig = False
            self.p.terminate()
            self.statusBar().showMessage("Pause")
            self.pause_or_start_Btn.setText("Go")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    App = APP()
    sys.exit(app.exec_())
