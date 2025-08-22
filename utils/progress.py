import psutil
import shutil

def generate_progress_bar(percent):
    filled = int(percent / 5)
    empty = 20 - filled
    return '⬢' * filled + ' ' * empty

def get_system_stats():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    free_bytes = shutil.disk_usage("/").free
    return cpu, ram, free_bytes

def format_size(size, show_bytes=True):
    # size en bytes
    if size < 1024:
        return f"{size} B" if show_bytes else "0.0 MB"
    elif size < 1024 ** 2:
        return f"{size / 1024:.2f} KB"
    elif size < 1024 ** 3:
        return f"{size / (1024 ** 2):.2f} MB"
    else:
        return f"{size / (1024 ** 3):.2f} GB"
