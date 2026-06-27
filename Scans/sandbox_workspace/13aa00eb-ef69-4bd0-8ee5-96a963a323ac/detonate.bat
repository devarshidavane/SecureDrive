@echo off
echo [Sandbox] Detonating esbuild.exe... > C:\Users\WDAGUtilityAccount\Desktop\Shared\sandbox_log.txt
start /wait "" "C:\Users\WDAGUtilityAccount\Desktop\Shared\esbuild.exe"
echo [Sandbox] Execution complete. Exit Code: %errorlevel% >> C:\Users\WDAGUtilityAccount\Desktop\Shared\sandbox_log.txt
echo [Sandbox] Done >> C:\Users\WDAGUtilityAccount\Desktop\Shared\sandbox_done.flag
