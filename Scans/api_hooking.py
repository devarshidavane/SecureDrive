import frida
import sys
import psutil
from pathlib import Path

# JavaScript payload to inject into the target process
HOOK_SCRIPT = """
// Hooking kernel32.dll!WriteFile
var kernel32 = Module.findBaseAddress('kernel32.dll');
var WriteFile = Module.findExportByName('kernel32.dll', 'WriteFile');

if (WriteFile) {
    Interceptor.attach(WriteFile, {
        onEnter: function (args) {
            // args[0] = hFile, args[1] = lpBuffer, args[2] = nNumberOfBytesToWrite
            var numBytes = args[2].toInt32();
            if (numBytes > 0) {
                // If attempting to write large amounts of data, could be ransomware behavior
                if (numBytes > 1024 * 1024) {
                    send({
                        type: 'alert',
                        api: 'WriteFile',
                        details: 'Large file write detected: ' + numBytes + ' bytes'
                    });
                }
            }
        }
    });
}

// Hooking advapi32.dll!RegSetValueExW
var advapi32 = Module.findBaseAddress('advapi32.dll');
var RegSetValueExW = Module.findExportByName('advapi32.dll', 'RegSetValueExW');

if (RegSetValueExW) {
    Interceptor.attach(RegSetValueExW, {
        onEnter: function (args) {
            // args[1] = lpValueName
            var valueName = Memory.readUtf16String(args[1]);
            send({
                type: 'alert',
                api: 'RegSetValueExW',
                details: 'Registry modification detected on key: ' + valueName
            });
        }
    });
}

send({ type: 'info', message: 'Hooks applied successfully.' });
"""

def on_message(message, data, target_pid):
    if message['type'] == 'send':
        payload = message['payload']
        if payload['type'] == 'alert':
            print(f"[SecureDrive] BEHAVIORAL ALERT [PID: {target_pid}]: API {payload['api']} -> {payload['details']}")
            # In a real NGAV, we would terminate the process here for severe violations.
            # psutil.Process(target_pid).kill()
        elif payload['type'] == 'info':
            print(f"[SecureDrive] {payload['message']}")
    elif message['type'] == 'error':
        print(f"[SecureDrive] Frida Error: {message['description']}")

def spawn_and_hook(executable_path):
    """
    Spawns the executable in a CREATE_SUSPENDED state, injects the hooks, and resumes it.
    """
    exe_path = str(Path(executable_path).absolute())
    print(f"[SecureDrive] Spawning and hooking: {exe_path}")
    
    try:
        # Spawn suspended
        pid = frida.spawn([exe_path])
        session = frida.attach(pid)
        
        # Inject script
        script = session.create_script(HOOK_SCRIPT)
        
        # Callback for messages from the injected script
        script.on('message', lambda msg, data: on_message(msg, data, pid))
        script.load()
        
        # Resume the suspended process
        frida.resume(pid)
        print(f"[SecureDrive] Process resumed (PID: {pid}). Monitoring APIs...")
        
        # Keep alive while process runs
        sys.stdin.read()
    except frida.NotSupportedError as e:
        print(f"[SecureDrive] Failed to hook (might need admin privileges): {e}")
    except Exception as e:
        print(f"[SecureDrive] Hooking error: {e}")

def attach_and_hook(pid):
    """
    Attaches to an already running process to monitor its APIs.
    """
    try:
        session = frida.attach(pid)
        script = session.create_script(HOOK_SCRIPT)
        script.on('message', lambda msg, data: on_message(msg, data, pid))
        script.load()
        print(f"[SecureDrive] Successfully attached to PID {pid}. Monitoring APIs...")
    except Exception as e:
        print(f"[SecureDrive] Failed to attach to PID {pid}: {e}")
