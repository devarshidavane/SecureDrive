@echo off
echo [Sandbox] Detonating esbuild.exe... > C:\Users\WDAGUtilityAccount\Desktop\Shared\sandbox_log.txt
:: Pipe nul to prevent CLI applications from hanging indefinitely waiting for stdin
"C:\Users\WDAGUtilityAccount\Desktop\Shared\esbuild.exe" < nul
echo [Sandbox] Execution complete. Exit Code: %errorlevel% >> C:\Users\WDAGUtilityAccount\Desktop\Shared\sandbox_log.txt
echo [Sandbox] Done >> C:\Users\WDAGUtilityAccount\Desktop\Shared\sandbox_done.flag
