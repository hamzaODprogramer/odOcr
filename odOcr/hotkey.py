import ctypes
from ctypes import wintypes
import threading
import time

WM_HOTKEY = 0x0312
MOD_CONTROL = 0x0002
MOD_NOREPEAT = 0x4000
VK_O = 0x4F

user32 = ctypes.windll.user32


class HotkeyListener:
    def __init__(self, on_hotkey, hotkey_mod=MOD_CONTROL, hotkey_vk=VK_O):
        self.on_hotkey = on_hotkey
        self.hotkey_mod = hotkey_mod
        self.hotkey_vk = hotkey_vk
        self.id = 1
        self._running = False
        self._thread = None

    def start(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._listen, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        try:
            user32.UnregisterHotKey(None, self.id)
        except Exception:
            pass

    def _listen(self):
        if not user32.RegisterHotKey(
            None, self.id, self.hotkey_mod | MOD_NOREPEAT, self.hotkey_vk
        ):
            return

        try:
            msg = wintypes.MSG()
            while self._running:
                ret = user32.GetMessageW(ctypes.byref(msg), None, 0, 0)
                if ret == 0:
                    break
                if ret == -1:
                    break
                if msg.message == WM_HOTKEY and msg.wParam == self.id:
                    if self.on_hotkey:
                        self.on_hotkey()
        finally:
            try:
                user32.UnregisterHotKey(None, self.id)
            except Exception:
                pass
