import psutil, shutil, os, subprocess, winreg, webbrowser, ctypes, sys

def run_as_admin():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        params = " ".join([sys.executable] + sys.argv)
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
        sys.exit()
        
def is_64bit():
        if os.name == 'nt':
            os_arch = os.environ["PROCESSOR_ARCHITEW6432"]
            return True if os_arch == 'AMD64' else False
        else:
            os._exit(0)
        return os_arch
    
def subprocess_handler(cmd):
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
	output = p.communicate()
	
	return [p.returncode, output]

def set_registry(keys):
    mask = winreg.KEY_WOW64_64KEY | winreg.KEY_ALL_ACCESS if is_64bit() else winreg.KEY_ALL_ACCESS

    for key_name, values in keys.items():
        try:
            key = winreg.CreateKeyEx(values[0], values[1], 0, mask)
            winreg.SetValueEx(key, values[2], 0, values[3], values[4])
            winreg.CloseKey(key)
            print("Registry: Successfully modified {key} key.".format(key=key_name))
        except OSError:
            print("Registry: Unable to modify {key} key.".format(key=key_name))

def empty_recycle_bin():
    try:
        SHEmptyRecycleBinW = ctypes.windll.shell32.SHEmptyRecycleBinW
        flags = 0
        result = SHEmptyRecycleBinW(None, None, flags)
        if result == 0:
            print("Empty the trash")
        else:
            print("[Error] Failed to empty the trash.")
    except Exception as e:
        print(f"[Error] Unable to empty the trash : {e}")
        
def erase_browser_login():
    login_paths = {
        "Chrome": os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data"),
        "Firefox": os.path.expanduser("~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\"),
        "Edge": os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Login Data"),
        "Brave": os.path.expanduser("~\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Login Data"),
    }
    
    for browser_name, path in login_paths.items():
        try:
            if browser_name == "Firefox":
                if os.path.exists(path):
                    for profile_folder in os.listdir(path):
                        login_file = os.path.join(path, profile_folder, "logins.json")
                        if os.path.exists(login_file):
                            os.remove(login_file)
                            print(f"[{browser_name}] Login data deleted for profile: {profile_folder}")
                else:
                    print(f"[{browser_name}] No profiles found.")
            else:
                if os.path.exists(path):
                    os.remove(path)
                    print(f"[{browser_name}] Données de connexion supprimées.")
                else:
                    print(f"[{browser_name}] No connection data found.")
        except Exception as e:
            print(f"[{browser_name}] Error deleting data: {e}")

def clean_browser_cache():
    """Nettoie les caches, cookies et historique des navigateurs courants."""
    paths = {
        "Chrome": {
            "cache": os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cache"),
            "cookies": os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cookies"),
            "history": os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History")
        },
        "Firefox": {
            "cache": os.path.expanduser("~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles"),
            "cookies": os.path.expanduser("~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles"),
            "history": os.path.expanduser("~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles")
        },
        "Edge": {
            "cache": os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Cache"),
            "cookies": os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Cookies"),
            "history": os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\History")
        },
        "Brave": {
            "cache": os.path.expanduser("~\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Cache"),
            "cookies": os.path.expanduser("~\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Cookies"),
            "history": os.path.expanduser("~\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default\\History")
        }
    }
    for browser, data in paths.items():
        for data_type, path in data.items():
            if os.path.exists(path):
                try:
                    if data_type in ["cache", "cookies"]:
                        shutil.rmtree(path, ignore_errors=True)
                    elif data_type == "history" and os.path.isfile(path):
                        os.remove(path)
                    print(f"{browser}: {data_type} nettoyé.")
                except Exception as e:
                    print(f"[Erreur] Échec lors du nettoyage de {browser} ({data_type}) : {e}")


class Tools:
    def __init__(self):
        pass
    
    def cpu_bouncer(): # A modifier pour qu'il tue les processus qui utilisent trop de CPU
        """This function kills processes that too much memory."""    
        for process in psutil.process_iter(attrs=['pid', 'name', 'memory_percent']):
            try:
                if process.info['memory_percent'] > 0.5: # Valeur à changer mais pour test / trouver quels process il faut kill et quels process il ne faut pas kill
                    process.kill()   
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                print(f'[Error]: {process}')
                pass
    
    def disk_space(drive="C:"):
        '''This function checks the disk space and sends a warning if the disk space is greater than 80%.'''
        usage = psutil.disk_usage(drive)
        if usage.percent > 80:
            print(f"Disk space warning! {usage.percent}% used on {drive}.")
        else :
            print(f'Disk space is OK. Only,{usage.percent}%, are used')
            
    def clean_local_temp():
        '''This function cleans the disk by deleting temporary files.'''  
        run_as_admin() 
        temp_dir = os.environ.get('TEMP', '')
        if os.path.exists(temp_dir):
            print(f"Cleaning temporary files in {temp_dir}...")
            for filename in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, filename)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        print(f"Deleted {file_path}")
                except PermissionError:
                    print(f"Permission denied: {file_path}")
                except Exception as e:
                    print(f"Error cleaning {file_path}: {e}")
        else:
            print(f"Temporary directory {temp_dir} does not exist.")
    
        prefetch_folder_path = os.path.join(os.environ['SystemRoot'], 'Prefetch')
        files = os.listdir(prefetch_folder_path)
        for file in files:
            file_path = os.path.join(prefetch_folder_path, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Error cleaning: {e}")

        print(f"Folder {prefetch_folder_path} has been cleared successfully.")
            
    def ultimate_power():
        command = "powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61"
        try:
            subprocess.run(command, shell=True, check=True)
            print(f'Power plan "Ultimate Performance" added successfully')
        except subprocess.CalledProcessError as e:
            print(f"Error setting power plan to Ultimate Performance: {e}")

                
    def telemetry():
        value = 0
        telemetry_keys = {'AllowTelemetry': [winreg.HKEY_LOCAL_MACHINE,
                                         r'SOFTWARE\Policies\Microsoft\Windows\DataCollection',
                                         "AllowTelemetry", winreg.REG_DWORD, value]}
        set_registry(telemetry_keys)
        
    def blackbird():
        url = "https://www.getblackbird.net/"
        webbrowser.open(url)
    def privacysexy():
        url = "https://privacy.sexy/"
        webbrowser.open(url)
    
    def onedrive():
        file_sync_value = 0
        list_pin_value = int(not 0)
        action = "install" if 0 else "uninstall"
        if is_64bit():
            onedrive_keys = {'FileSync': [winreg.HKEY_LOCAL_MACHINE,
									  r'SOFTWARE\Policies\Microsoft\Windows\OneDrive',
									  'DisableFileSyncNGSC', winreg.REG_DWORD, file_sync_value],

						 'ListPin': [winreg.HKEY_CLASSES_ROOT,
									 r'CLSID\{018D5C66-4533-4307-9B53-224DE2ED1FE6}',
									 'System.IsPinnedToNameSpaceTree', winreg.REG_DWORD, list_pin_value],

						 'ListPin64Bit': [winreg.HKEY_CLASSES_ROOT,
									 r'Wow6432Node\CLSID\{018D5C66-4533-4307-9B53-224DE2ED1FE6}',
									 'System.IsPinnedToNameSpaceTree', winreg.REG_DWORD, list_pin_value]}
        else:	
            onedrive_keys = {'FileSync': [winreg.HKEY_LOCAL_MACHINE,
									  r'SOFTWARE\Policies\Microsoft\Windows\OneDrive',
									  'DisableFileSyncNGSC', winreg.REG_DWORD, file_sync_value],

						 'ListPin': [winreg.HKEY_CLASSES_ROOT,
									 r'CLSID\{018D5C66-4533-4307-9B53-224DE2ED1FE6}',
									 'System.IsPinnedToNameSpaceTree', winreg.REG_DWORD, list_pin_value]}
        set_registry(onedrive_keys)
        system = "SysWOW64" if is_64bit() else "System32"
        onedrive_setup = os.path.join(os.environ['SYSTEMROOT'], "{system}\\OneDriveSetup.exe".format(system=system))
        cmd = "{bin} /{action}".format(bin=onedrive_setup, action=action)
        output = subprocess_handler(cmd)
        if output[0] == -2147219823:
            print("[OneDrive]: successfully {action}ed".format(action=action))
        else:
            print("[OneDrive]: unable to {action}. Exited with code: {code} - {message}".format(action=action, code=output[0], message=output[1]))
    
    
    def disk_cleaner():
        run_as_admin()
        erase_browser_login()
        clean_browser_cache()
        empty_recycle_bin()
        

