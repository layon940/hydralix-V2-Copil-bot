import psutil
import shutil

def generate_progress_bar(percent):
    filled = int(percent / 5)
    empty = 20 - filled
    return '⬢' * filled + ' ' * empty

def get_system_stats():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    free = round(shutil.disk_usage("/").free / (1024**3), 2)
    return cpu, ram, free
