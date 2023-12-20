from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
import subprocess
from RedisCache_module import getRedis

class Genuinity(QWidget):
    def __init__(self, sudo_password):
        super(Genuinity, self).__init__()

        self.sudo_password = sudo_password

        layout = QVBoxLayout()

        authenticate_button = QPushButton('Authenticate')
        authenticate_button.clicked.connect(self.run_update_script)
        layout.addWidget(authenticate_button)

        self.result_label = QLabel('')  # Label to display the result of the executed scripts
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def run_script(self, command):
        full_command = f"{getRedis(1)} {self.sudo_password} | {getRedis(2)} {command}"
        result = subprocess.run(full_command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            self.result_label.setText(result.stdout)
        else:
            self.result_label.setText(f"Error: {result.stderr}")

    def run_authenticate_script(self):
        authenticate_script = {getRedis(4)}

        self.run_script(authenticate_script)





