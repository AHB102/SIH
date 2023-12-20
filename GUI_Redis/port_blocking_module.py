from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSizePolicy
import subprocess
import tempfile
import os
from RedisCache_module import getRedis

class PortBlocking(QWidget):
    def __init__(self, sudo_password):
        super(PortBlocking, self).__init__()

        self.sudo_password = sudo_password

        layout = QVBoxLayout()
        intro_label = QLabel("Prevents unauthorized USB devices from connecting, enhancing security by controlling physical access to the system.")
        intro_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        intro_label.setWordWrap(True)
        layout.addWidget(intro_label)

        disable_button = QPushButton('Disable')
        disable_button.setToolTip('Disables all USB ports by setting authorized flag to 0 for each port.')
        disable_button.clicked.connect(self.run_disable_script)
        layout.addWidget(disable_button)

        enable_button = QPushButton('Enable')
        enable_button.setToolTip('Enables all USB ports by setting authorized flag to 1 for each port.')

        enable_button.clicked.connect(self.run_enable_script)
        layout.addWidget(enable_button)

        self.result_label = QLabel('')  # Label to display the result of the executed scripts
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def run_script(self, script):
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            temp_file.write(script)
            temp_file_path = temp_file.name

        try:
            full_command = f"{getRedis(1)} {self.sudo_password} | {getRedis(2)} {getRedis(5)} {temp_file_path}"
            result = subprocess.run(full_command, shell=True, capture_output=True, text=True)

            if result.returncode == 0:
                self.result_label.setText(result.stdout)
            else:
                self.result_label.setText(f"Error: {result.stderr}")

        finally:
            os.remove(temp_file_path)

    def run_disable_script(self):
        disable_script = getRedis(6)
        with open('script.sh', 'a') as file:
            # Write content to the file
            file.write(f"{getRedis(6)}\n")
        self.run_script(disable_script)

    def run_enable_script(self):
        enable_script = getRedis(7)
        with open('script.sh', 'a') as file:
            # Write content to the file
            file.write(f"{getRedis(7)}\n")
        self.run_script(enable_script)
