' Run a command with no window and wait for it; exit with its code.
' Used by the scheduled tasks (scripts/ops/install_schedule.ps1).
' Usage: wscript.exe //B //Nologo hidden.vbs PROGRAM [ARG ...]
Set sh = CreateObject("WScript.Shell")
cmd = ""
For Each a In WScript.Arguments
    cmd = cmd & " """ & a & """"
Next
WScript.Quit sh.Run(Trim(cmd), 0, True)
