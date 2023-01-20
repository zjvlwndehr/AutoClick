import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import win32api, win32con
from time import sleep
from random import randint
from math import pow

from threading import Thread

class Mouse:
    def __init__(self) -> None:
        self.right_key_bind = 'X1BUTTON'
        self.left_key_bind = 'X2BUTTON'
        self.LInterval = 0.041
        self.RInterval = 0.021
        self.use_right_click = False
        self.Trig = False
        self.random_list = []
        for _ in range(100):
            self.random_list.append(randint(0, 10)/1000)

    def click(self, x,y, button = "left"):
        win32api.SetCursorPos((x,y))
        if button == "left":
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
            sleep(0.01+(-1)**(randint(0, 1))*self.random_list[randint(0, 99)])
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
        elif button == "right":
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
            sleep(0.01+pow(-1, randint(0, 1))*self.random_list[randint(0, 99)])
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)

    def proc(self) -> int:
        while self.Trig:
            if self.use_right_click == True:
                x,y = win32api.GetCursorPos()
                if win32api.GetAsyncKeyState(win32con.VK_XBUTTON2):
                    self.click(x,y, button = "left")
                    sleep(self.LInterval+(-1)**(randint(0, 1))*self.random_list[randint(0, 99)])
                if win32api.GetAsyncKeyState(win32con.VK_XBUTTON1):
                    self.click(x,y, button = "right")
                    sleep(self.RInterval+(-1)**(randint(0, 1))*self.random_list[randint(0, 99)])
            elif self.use_right_click == False:
                if win32api.GetAsyncKeyState(win32con.VK_XBUTTON2) or win32api.GetAsyncKeyState(win32con.VK_XBUTTON1):
                    x,y = win32api.GetCursorPos()
                    self.click(x,y, button = "left")
                    sleep(self.LInterval)
        return 0

class APP(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.mouse = Mouse()
        self.icon = QIcon('resources/ico.jpg')
        self.pause_or_start_Btn = QPushButton("", self)
        self.pause_or_start_Btn.setText("Go")
        self.UseRclickLabel = QLabel("Use Right click", self)
        self.UseRclickCheckBox = QCheckBox(self)
        self.RightKeyBindingLabel = QLabel("Right click key bind", self)
        self.RightKeyBindingLabel.setText(self.RightKeyBindingLabel.text() + "\t: " + 'None')
        self.LeftKeyBindingLabel = QLabel("Left click key bind", self)
        self.LeftKeyBindingLabel.setText(self.LeftKeyBindingLabel.text() + "\t: " + self.mouse.left_key_bind + "\n" + self.mouse.right_key_bind)
        self.t = Thread(target=self.mouse.proc, daemon=True)
        self.t_list = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Just a tool")
        self.setWindowIcon(QIcon('resources/ico.jpg'))
        self.setWindowFlags(Qt.WindowMinimizeButtonHint)
        self.statusBar().showMessage("Pause")
        w = 300
        h = 150

        self.setFixedSize(w, h)
        self.setGeometry(300, 300, w, h)
        
        self.icon.addPixmap(QPixmap("resources/ico.jpg"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(self.icon)

        self.pause_or_start_Btn.setToolTip("Pause the application")
        self.pause_or_start_Btn.setGeometry(int((w-100)/2)+70, int((h-50)/2), 100, 50)
        self.pause_or_start_Btn.clicked.connect(self.pause_or_start)

        self.UseRclickLabel.setGeometry(10, 50, 100, 20)
        self.UseRclickCheckBox.setGeometry(100, 50, 20, 20)
        self.UseRclickCheckBox.stateChanged.connect(self.UseRclickCheckBoxChanged)

        self.RightKeyBindingLabel.setGeometry(10, 80, 200, 40)
        self.LeftKeyBindingLabel.setGeometry(10, 100, 200, 40)

        exitAction = QAction(QIcon('resources/exit.png'), 'Exit', self)
        exitAction.setShortcut('Alt+F4')
        exitAction.triggered.connect(self.exitActionBtnClicked)

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
        self.restart()
    
    def pause_or_start(self):
        if self.statusBar().currentMessage() == "Pause":
            self.mouse.Trig = True
            self.t.start()
            self.t_list.append(self.t)
            self.statusBar().showMessage("Running...")
            self.pause_or_start_Btn.setText("Pause")
        else:
            self.mouse.Trig = False
            self.t.join()
            self.t_list = []
            self.t = Thread(target=self.mouse.proc, daemon=True)

            self.statusBar().showMessage("Pause")
            self.pause_or_start_Btn.setText("Go")

    def restart(self):
        print("restart")
        print(self.t_list)
        if self.t_list == []:
            pass
        else:
            self.mouse.Trig = False
            self.t.join()
            self.t_list = []
            self.mouse.Trig = True
            self.t = Thread(target=self.mouse.proc, daemon=True)
            self.t.start()
            self.t_list.append(self.t)

    def exitActionBtnClicked(self):
        if self.t_list == []:
            pass
        else:
            try:
                self.p.terminate()
            except:
                pass
            self.t_list = []
            self.t = None
        qApp.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    App = APP()
    sys.exit(app.exec_())
