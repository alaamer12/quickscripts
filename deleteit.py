import os
import shutil
import ctypes
import sys
import subprocess
from ctypes import windll
import time
import winreg


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    if not is_admin():
        windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()


def disable_self_protection():
    try:
        # Try to disable Avast self-protection through registry
        key_path = r"SOFTWARE\AVAST Software\Avast"
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_ALL_ACCESS)
            winreg.SetValueEx(key, "SelfDefense", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
        except Exception as e:
            print(f"Registry modification failed: {e}")

        # Try to disable through command line tool if available
        subprocess.run(['sc', 'stop', "aswSP"], shell=True, capture_output=True)
        
    except Exception as e:
        print(f"Error disabling self-protection: {e}")


def stop_avast_services():
    try:
        # More comprehensive list of services
        avast_services = [
            "AvastSvc",
            "AvastWcfSvc",
            "aswBcc",
            "aswEngSrv",
            "aswMonFlt",
            "aswVmm",
            "aswSP",
            "aswbIDSAgent",
            "aswElam",
            "aswHdsKe",
        ]
        
        # Stop services using both sc and net commands
        for service in avast_services:
            subprocess.run(['sc', 'stop', service], shell=True, capture_output=True)
            subprocess.run(['net', 'stop', service], shell=True, capture_output=True)
            
        # Extended list of processes
        avast_processes = [
            "AvastSvc.exe",
            "AvastUI.exe",
            "aswEngSrv.exe",
            "aswidsagent.exe",
            "ashServ.exe",
            "AvastBrowser.exe",
            "wsc_proxy.exe",
            "aswToolsSvc.exe",
            "AvastSecureBrowser.exe"
        ]
        
        # Kill processes with different methods
        for process in avast_processes:
            subprocess.run(['taskkill', '/F', '/IM', process], shell=True, capture_output=True)
            subprocess.run(['tskill', process], shell=True, capture_output=True)
        
        # Additional system-level termination
        subprocess.run(['sc', 'delete', "AvastSvc"], shell=True, capture_output=True)
        time.sleep(3)
        return True
    except Exception as e:
        print(f"Error stopping services: {e}")
        return False


def take_ownership(path):
    try:
        # Take ownership recursively
        subprocess.run(['takeown', '/f', path, '/r', '/d', 'y'], capture_output=True)
        
        # Grant full permissions using different methods
        subprocess.run(['icacls', path, '/grant', 'administrators:F', '/t', '/c', '/l'], capture_output=True)
        subprocess.run(['icacls', path, '/grant', 'Users:F', '/t', '/c', '/l'], capture_output=True)
        subprocess.run(['attrib', '-r', '-s', '-h', '/s', '/d', path], shell=True, capture_output=True)
        
        # Try to reset permissions completely
        subprocess.run(['icacls', path, '/reset', '/t'], capture_output=True)
        return True
    except Exception as e:
        print(f"Error taking ownership: {e}")
        return False


def force_delete_windows_directory(path):
    try:
        run_as_admin()
        path = os.path.normpath(path)
        
        if not os.path.exists(path):
            print(f"Path does not exist: {path}")
            return False

        # Try to disable protection first
        disable_self_protection()
        
        # Take ownership with multiple attempts
        for _ in range(3):
            take_ownership(path)
            time.sleep(1)

        def remove_readonly(path):
            try:
                ctypes.windll.kernel32.SetFileAttributesW(path, 128)
                subprocess.run(['attrib', '-r', '-s', '-h', path], shell=True, capture_output=True)
            except Exception as attr_error:
                print(f"Could not remove attributes: {attr_error}")

        def remove_dir_contents(directory):
            # Try to unload DLLs first
            subprocess.run(['taskkill', '/F', '/IM', '*avast*'], shell=True, capture_output=True)
            
            for root, dirs, files in os.walk(directory, topdown=False):
                for name in files:
                    file_path = os.path.join(root, name)
                    try:
                        remove_readonly(file_path)
                        if os.path.exists(file_path):
                            os.chmod(file_path, 0o777)
                            # Try multiple deletion methods
                            try: os.unlink(file_path)
                            except: pass
                            try: subprocess.run(['del', '/f', '/q', file_path], shell=True)
                            except: pass
                            try: shutil.rmtree(file_path, ignore_errors=True)
                            except: pass
                    except Exception as file_error:
                        print(f"Could not delete file {file_path}: {file_error}")

                for name in dirs:
                    dir_path = os.path.join(root, name)
                    try:
                        remove_readonly(dir_path)
                        if os.path.exists(dir_path):
                            os.chmod(dir_path, 0o777)
                            try: os.rmdir(dir_path)
                            except: pass
                            try: subprocess.run(['rmdir', '/s', '/q', dir_path], shell=True)
                            except: pass
                            try: shutil.rmtree(dir_path, ignore_errors=True)
                            except: pass
                    except Exception as dir_error:
                        print(f"Could not delete directory {dir_path}: {dir_error}")

        # Multiple deletion attempts
        for attempt in range(3):
            print(f"Deletion attempt {attempt + 1}...")
            remove_dir_contents(path)
            time.sleep(2)

            if os.path.exists(path):
                remove_readonly(path)
                try: os.rmdir(path)
                except: pass
                try: subprocess.run(['rmdir', '/s', '/q', path], shell=True)
                except: pass
                try: shutil.rmtree(path, ignore_errors=True)
                except: pass

            if not os.path.exists(path):
                print(f"Successfully deleted directory: {path}")
                return True

        print("Directory still exists after all attempts")
        return False

    except Exception as e:
        print(f"Error deleting directory {path}: {e}")
        return False


def main():
    target_directory = r"F:\Program Files\Avast Software"
    print("Stopping Avast services...")
    stop_avast_services()
    print("Attempting deletion...")
    force_delete_windows_directory(target_directory)


if __name__ == "__main__":
    main()