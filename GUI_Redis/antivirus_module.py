from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSizePolicy
import subprocess
from RedisCache_module import getRedis


class AntiVirusModule(QWidget):
    def __init__(self, sudo_password):
        super(AntiVirusModule, self).__init__()

        self.sudo_password = sudo_password

        layout = QVBoxLayout()
        intro_label = QLabel("Scans for and detects malicious software, protecting the system from viruses and spyware threats.")
        intro_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        intro_label.setWordWrap(True)
        layout.addWidget(intro_label)



        check_button = QPushButton('Check Installation')
        check_button.setToolTip('Checks for the availability of popular antivirus and anti-spyware tools.')
        check_button.clicked.connect(self.run_check_script)
        layout.addWidget(check_button)

        install_button = QPushButton('Install Antivirus')
        install_button.setToolTip('Installs popular antivirus and anti-spyware tools.')
        install_button.clicked.connect(self.run_install_script)
        layout.addWidget(install_button)

        self.result_label = QLabel('')  # Label to display the result of the executed scripts
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def run_script(self, command):
        full_command = f"{getRedis(1)} '{self.sudo_password}' | {getRedis(11)} '{command}'"
        result = subprocess.run(full_command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            self.result_label.setText(result.stdout)
        else:
            self.result_label.setText(f"Error: {result.stderr}")

    def run_check_script(self):
        self.run_script({getRedis(8)})
        with open('script.sh', 'a') as file:
            # Write content to the file
            file.write(f"{getRedis(8)}\n")

    def run_install_script(self):
        self.run_script(getRedis(9))
        with open('script.sh', 'a') as file:
            # Write content to the file
            file.write(f"{getRedis(9)}\n")



