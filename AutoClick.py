#ketchup2480@gmail.com
#github :zjvlwndehr
#©2020

import pyautogui as pag # 메크로 이벤트 생성
import keyboard as kb   # 키(개별) 입력
import os               # 프로그램 종료
import pygame           # 클릭 틱 조정


def esc():
    print("종료")
    os._exit(1)   

    
while(1): 
    if kb.is_pressed('f'):
        while(1):
            currentMouseX, currentMouseY = pag.position()
            pag.click(currentMouseX, currentMouseY,button='left')
            if kb.is_pressed('ctrl'):
                if kb.is_pressed('c'):
                    esc()
            if kb.is_pressed('f'):
                break
    if kb.is_pressed('v'):
        while(1):
            currentMouseX, currentMouseY = pag.position()
            pag.click(currentMouseX, currentMouseY,button='right')
            if kb.is_pressed('ctrl'):
                if kb.is_pressed('c'):
                    esc()
            if kb.is_pressed('c'):
                break