import os

SYSTEM_D_FILE = "doctor-search-beep.service"
PWD = os.getcwd()

env = input("Env folder? (used to execute service): ")

env_dir = os.path.join(PWD, env, "bin", "python")

template = f"""[Unit]
Description=This service periodically checks if there are free apointments for doctors
After=network-online.target

[Service]
ExecStart={env_dir} search_doctor.py
Restart=always
RestartSec=30min

[Install]
WantedBy=multi-user.target
"""

with open(SYSTEM_D_FILE, "w") as f:
    f.write(template)