import platform
import os
import shutil

SYSTEM_D_FILE = "doctor-search-beep.service"
SYSTEM_D_SERVICES_FILE = os.path.join("/", "etc", "systemd", "system", SYSTEM_D_FILE)

PWD = os.getcwd()

env = input("Env folder? (used to execute service): ")

env_dir = os.path.join(PWD, env, "bin", "python")
script_dir = os.path.join(PWD, "doctor-search-beep.py")

template = f"""[Unit]
Description=This service periodically checks if there are free apointments for doctors
After=network-online.target

[Service]
ExecStart={env_dir} {script_dir}
Restart=always
RestartSec=30min

[Install]
WantedBy=multi-user.target
"""

with open(SYSTEM_D_FILE, "w") as f:
    f.write(template)

if platform.system() == 'Linux':
    move = input("Move files to systemd directory? [y/n] (y): ")
    if move.upper() == 'Y':
        shutil.move(SYSTEM_D_FILE, SYSTEM_D_SERVICES_FILE)
else:
    print("File created but not moved because system is ", platform.system())
