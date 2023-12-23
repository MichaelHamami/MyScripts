import sys
from pywinauto.application import Application
import time
import pyautogui
import os

app_path = r'C:\Riot Games\Riot Client\RiotClientServices.exe'
play_button_path = r'C:\Michael\Projects\Scripts\AutoLogin\play_leage_of_legends.PNG'
game_choice_path = r'C:\Michael\Projects\Scripts\AutoLogin\leage_of_legends_choice.PNG'


def click_button(image_path, confidence=0.8):
    button_location = pyautogui.locateOnScreen(image_path, confidence=confidence)

    if button_location is not None:
        button_x, button_y = pyautogui.center(button_location)

        pyautogui.click(button_x, button_y)
        return True
    else:
        return False


def main():
    if os.name == 'nt':
        os.system(f'taskkill /f /im LeagueClient.exe')
        os.system(f'taskkill /f /im RiotClientUx.exe')
        os.system(f'taskkill /f /im RiotClientServices.exe')

    username = "someusername"
    password = "somepassword"

    if not (username and password):
        sys.exit(1)

    Application(backend='uia').start(app_path)
    time.sleep(5)

    pyautogui.typewrite(username)
    pyautogui.press('tab')
    pyautogui.typewrite(password)
    pyautogui.press('enter')

    time.sleep(5)

    if click_button(game_choice_path) is False:
        return

    time.sleep(2)
    click_button(play_button_path)


if __name__ == '__main__':
    main()