import psutil
import os


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
                pass
    
    
    def disk_space(self, drive="C:"):
        '''This function checks the disk space and sends a warning if the disk space is greater than 80%.'''
        usage = psutil.disk_usage(drive)
        if usage.percent > 80:
            print(f"Disk space warning! {usage.percent}% used on {drive}.")
        else :
            print('Disk space is OK. Only, {usage.percent}%, are used')
            
         
    def disk_cleaner(self):
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

tool = Tools()


