import platform
import psutil

def get_system_profile():
    """
    Fetches OS details, total/available RAM, and CPU core counts.
    """
    profile = {
        "os": platform.system(),
        "os_release": platform.release(),
        "os_version": platform.version(),
        "cpu_cores_physical": psutil.cpu_count(logical=False),
        "cpu_cores_logical": psutil.cpu_count(logical=True),
        "total_ram_gb": psutil.virtual_memory().total / (1024 ** 3),
        "available_ram_gb": psutil.virtual_memory().available / (1024 ** 3)
    }
    return profile

def get_optimal_thread_count():
    """
    Dynamically adjusts internal resource usage (like maximum concurrent scan threads)
    to prevent system slowdowns during a full scan.
    """
    profile = get_system_profile()
    
    # Base calculation on physical cores to avoid overwhelming the scheduler
    cores = profile.get("cpu_cores_physical") or 4
    
    available_ram = profile.get("available_ram_gb", 0)
    
    # If we have less than 2GB of free RAM, throttle significantly
    if available_ram < 2.0:
        return max(1, cores // 2)
    
    # If we have plenty of RAM (e.g., > 8GB available), we can use more threads
    if available_ram > 8.0:
        return cores * 2
        
    # Standard fallback
    return cores
