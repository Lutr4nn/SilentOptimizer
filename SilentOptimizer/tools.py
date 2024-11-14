import psutil

class Tools:
    
    def __init__(self):
        pass
        
    def cpu_bouncer(self):
        """This function kills processes that too much memory."""
        
        for process in psutil.process_iter(attrs=['pid', 'name', 'memory_percent']):
            try:
                if process.info['memory_percent'] > 0.5: # Valeur à changer mais pour test / trouver quels process il faut kill et quels process il ne faut pas kill
                    process.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass


tool = Tools()

