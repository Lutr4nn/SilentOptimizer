import psutil, shutil, os, subprocess, winreg, webbrowser

def is_64bit():
        if os.name == 'nt':
            os_arch = os.environ["PROCESSOR_ARCHITEW6432"]
            return True if os_arch == 'AMD64' else False
        else:
            os._exit(0)
        return os_arch
    
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
            
            
class Tools:
    def __init__(self):
        pass
    
    def cpu_bouncer(self): # A modifier pour qu'il tue les processus qui utilisent trop de CPU
        """This function kills processes that too much memory."""    
        for process in psutil.process_iter(attrs=['pid', 'name', 'memory_percent']):
            try:
                if process.info['memory_percent'] > 0.5: # Valeur à changer mais pour test / trouver quels process il faut kill et quels process il ne faut pas kill
                    process.kill()   
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                print(f'Error: {process}')
                pass
    
    def disk_space(self, drive="C:"):
        '''This function checks the disk space and sends a warning if the disk space is greater than 80%.'''
        usage = psutil.disk_usage(drive)
        if usage.percent > 80:
            print(f"Disk space warning! {usage.percent}% used on {drive}.")
        else :
            print(f'Disk space is OK. Only,{usage.percent}%, are used')
            
    def clean_local_temp(self):
        '''This function cleans the disk by deleting temporary files.'''   
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

                
    def telemetry(undo):
        value = int(undo)
        telemetry_keys = {'AllowTelemetry': [winreg.HKEY_LOCAL_MACHINE,
                                         r'SOFTWARE\Policies\Microsoft\Windows\DataCollection',
                                         "AllowTelemetry", winreg.REG_DWORD, value]}
        set_registry(telemetry_keys)
        
    def privacysexy():
        url = "https://privacy.sexy/"
        webbrowser.open(url)
    
tool = Tools()


