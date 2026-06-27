import os
import shutil
import subprocess
import time
import uuid
from pathlib import Path

# Paths
SANDBOX_WORKSPACE = Path(__file__).parent / "sandbox_workspace"

def create_sandbox_workspace():
    if not SANDBOX_WORKSPACE.exists():
        SANDBOX_WORKSPACE.mkdir(parents=True)
    return SANDBOX_WORKSPACE

def generate_wsb(shared_folder, script_name):
    """
    Generates a .wsb XML configuration for Windows Sandbox.
    Maps the shared folder with Read/Write access so the sandbox can write logs back.
    """
    wsb_content = f"""<Configuration>
  <MappedFolders>
    <MappedFolder>
      <HostFolder>{shared_folder}</HostFolder>
      <SandboxFolder>C:\\Users\\WDAGUtilityAccount\\Desktop\\Shared</SandboxFolder>
      <ReadOnly>false</ReadOnly>
    </MappedFolder>
  </MappedFolders>
  <LogonCommand>
    <Command>cmd.exe /c "C:\\Users\\WDAGUtilityAccount\\Desktop\\Shared\\{script_name}"</Command>
  </LogonCommand>
</Configuration>"""
    
    wsb_path = Path(shared_folder) / "sandbox.wsb"
    with open(wsb_path, "w") as f:
        f.write(wsb_content)
    return wsb_path

def generate_detonator_script(target_exe):
    """
    Generates a basic batch script that runs the target executable,
    logs its exit status, and saves a basic behavioral log back to the host.
    """
    script_content = f"""@echo off
echo [Sandbox] Detonating {target_exe}... > C:\\Users\\WDAGUtilityAccount\\Desktop\\Shared\\sandbox_log.txt
:: Pipe nul to prevent CLI applications from hanging indefinitely waiting for stdin
"C:\\Users\\WDAGUtilityAccount\\Desktop\\Shared\\{target_exe}" < nul
echo [Sandbox] Execution complete. Exit Code: %errorlevel% >> C:\\Users\\WDAGUtilityAccount\\Desktop\\Shared\\sandbox_log.txt
echo [Sandbox] Done >> C:\\Users\\WDAGUtilityAccount\\Desktop\\Shared\\sandbox_done.flag
"""
    return script_content

def detonate_in_sandbox(file_path):
    """
    Dynamically generates a Windows Sandbox environment to safely detonate an executable.
    """
    file_path = Path(file_path)
    if not file_path.exists():
        return False, "File not found."

    workspace = create_sandbox_workspace()
    
    # Create unique session folder
    session_id = str(uuid.uuid4())
    session_dir = workspace / session_id
    session_dir.mkdir()

    # Copy suspicious file
    target_exe = session_dir / file_path.name
    shutil.copy2(file_path, target_exe)

    # Generate scripts and configs
    detonator_path = session_dir / "detonate.bat"
    with open(detonator_path, "w") as f:
        f.write(generate_detonator_script(file_path.name))

    wsb_path = generate_wsb(str(session_dir.absolute()), "detonate.bat")

    print(f"[SecureDrive] Launching Windows Sandbox for {file_path.name}...")
    
    # Launch Sandbox (Non-blocking so we can monitor)
    try:
        subprocess.Popen(["WindowsSandbox.exe", str(wsb_path.absolute())], shell=True)
    except Exception as e:
        return False, f"Failed to start sandbox: {e}"

    # Wait for completion flag or timeout (max 30 seconds for this demo)
    flag_file = session_dir / "sandbox_done.flag"
    log_file = session_dir / "sandbox_log.txt"
    
    timeout = 30
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        if flag_file.exists():
            break
        time.sleep(1)
        
    # Read results
    if log_file.exists():
        with open(log_file, "r") as f:
            log_content = f.read()
    else:
        log_content = "Timeout or execution failure. Process might have hung."
        
    # Clean up (Sandbox closes itself if user exits, but we can kill it or leave it)
    # Removing session dir cleans up our host files.
    # Note: Windows Sandbox instance stays open for the user to view unless programmatically killed,
    # but the task requirements just ask to run it and get logs.
    
    try:
        shutil.rmtree(session_dir, ignore_errors=True)
    except:
        pass
        
    return True, log_content
