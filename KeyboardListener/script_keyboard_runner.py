import os
import subprocess
import sys
import keyboard
import win32api
import win32con
import win32gui


class SystemTrayIcon:
    def __init__(self, hover_text, menu_options,
                 window_class_name="SysTrayIconPy"):
        self.hover_text = hover_text
        self.window_class_name = window_class_name

        menu_options_list = list(menu_options)
        menu_options_list.append((len(menu_options_list), "Exit", self.destroy, 'ctrl+0'))
        self.menu_options = tuple(menu_options_list)

        message_map = {
            win32gui.RegisterWindowMessage("TaskbarCreated"): self.restart,
            win32con.WM_DESTROY: self.destroy,
            win32con.WM_COMMAND: self.command_handler,
            win32con.WM_USER + 20: self.notify,
        }

        # Register the window class.
        wc = win32gui.WNDCLASS()

        hinst = wc.hInstance = win32api.GetModuleHandle(None)
        wc.lpszClassName = self.window_class_name
        wc.lpfnWndProc = message_map
        class_atom = win32gui.RegisterClass(wc)

        # Create the window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow(
            class_atom, self.window_class_name, style, 0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, 0, 0,
            hinst, None
        )

        win32gui.UpdateWindow(self.hwnd)
        self.notify_id = None
        self.refresh_icon()

        # Set up keyboard listener
        self.keyboard_hook = keyboard.hook(self.on_key_event)

    def refresh_icon(self):

        hinst = win32api.GetModuleHandle(None)
        if self.notify_id:
            message = win32gui.NIM_MODIFY
        else:
            message = win32gui.NIM_ADD

        icon = os.path.abspath("C:\\Michael\\Projects\\KeyboardListener\\git-gui.ico")

        flags = win32gui.LR_LOADFROMFILE | win32gui.LR_DEFAULTSIZE | win32gui.LR_LOADTRANSPARENT
        hicon = win32gui.LoadImage(hinst, icon, win32gui.IMAGE_ICON, 0, 0, flags)

        notify_flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP
        self.notify_id = (self.hwnd, 0, notify_flags, win32con.WM_USER + 20, hicon, self.hover_text)
        win32gui.Shell_NotifyIcon(message, self.notify_id)

    def restart(self, hwnd, msg, wparam, lparam):
        self.refresh_icon()

    def destroy(self, hwnd=None, msg=None, wparam=None, lparam=None):
        try:
            keyboard.unhook(self.keyboard_hook)
            nid = (self.hwnd, 0)
            win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
            win32gui.PostQuitMessage(0)
            sys.exit()
        except:
            print("error")

    def notify(self, hwnd, msg, wparam, lparam):
        if lparam == win32con.WM_RBUTTONUP:
            self.show_menu()
        elif lparam == win32con.WM_LBUTTONUP:
            pass
        return True

    def command_handler(self, hwnd, msg, wparam, lparam):
        self.execute_menu_option(wparam)
        return True

    def get_index_of_pressed_command(self, options):
        for index, (menu_index, _, _, command) in enumerate(options):
            if keyboard.is_pressed(command):
                return menu_index

        return -1

    def on_key_event(self, event):
        if event.event_type == keyboard.KEY_DOWN:
            index_of_menu_command = self.get_index_of_pressed_command(self.menu_options)
            if index_of_menu_command > -1:
                self.execute_menu_option(index_of_menu_command)

    def execute_menu_option(self, menu_index):
        menu_id, menu_item, functioncall, command = self.menu_options[menu_index]
        functioncall()

    def show_menu(self):
        menu = win32gui.CreatePopupMenu()
        for index, (menu_id, menu_item, _, _) in enumerate(self.menu_options):
            win32gui.AppendMenu(
                menu, win32con.MF_STRING, menu_id, menu_item
            )

        pos = win32gui.GetCursorPos()
        win32gui.SetForegroundWindow(self.hwnd)
        win32gui.TrackPopupMenu(
            menu, win32con.TPM_LEFTALIGN, pos[0], pos[1], 0, self.hwnd, None
        )
        win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)

        win32gui.DestroyMenu(menu)


def change_audio():
    print("change_audio called")
    script_path = r'C:\Michael\Projects\Scripts\audio_change.ps1'
    try:
        subprocess.run(['powershell.exe', '-File', script_path])
    except subprocess.CalledProcessError as e:
        print(f"Error executing script: {e}")


def login_lol(file_name):
    print("login_lol called", file_name)
    script_path = r'C:\Users\hamam\Desktop\{}.exe'.format(file_name)
    run_file(script_path)


def login_lol_calculated():
    file_name = r'Calculated'
    login_lol(file_name)


def login_lol_kal_arams():
    file_name = r'KalArams'
    login_lol(file_name)


def run_file(file_path):
    try:
        subprocess.Popen([file_path])
    except subprocess.CalledProcessError as e:
        print(f"Error executing script: {e}")


def join_discord():
    print("join_discord called")


def main():
    hover_text = "Script Runner"
    menu_options = (
        (0, "Change Audio", change_audio, 'ctrl+1'),
        (1, "Join Discord", join_discord, 'ctrl+2'),
        (2, "Login to Calculated", login_lol_calculated, 'ctrl+3'),
        (3, "Login to KalArams", login_lol_kal_arams, 'ctrl+4'),

    )

    SystemTrayIcon(hover_text, menu_options)

    win32gui.PumpMessages()


if __name__ == '__main__':
    main()
