from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSizePolicy
import subprocess
from RedisCache_module import getRedis
class BlockDNSModule(QWidget):
    def __init__(self, sudo_password):
        super(BlockDNSModule, self).__init__()

        self.sudo_password = sudo_password

        layout = QVBoxLayout()
        intro_label = QLabel("Welcome to the AntiVirus Module. Click the buttons below to check the installation "
                             "status or install antivirus tools.")
        intro_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        intro_label.setWordWrap(True)
        layout.addWidget(intro_label)

        blockDNSPort_button = QPushButton('Block DNS Port')
        blockDNSPort_button.setToolTip('Blocks all ports through which DNS traffic flows.')
        blockDNSPort_button.clicked.connect(self.run_blockDNSport_script)
        layout.addWidget(blockDNSPort_button)

        blockDNSProtocol_button = QPushButton('Block DNS Protocol')
        blockDNSProtocol_button.setToolTip('blocks Packets using DNS protocol.')

        blockDNSProtocol_button.clicked.connect(self.run_blockDNSprotocol_script)
        layout.addWidget(blockDNSProtocol_button)

        UnblockDNSPort_button = QPushButton('Unblock DNS Port')
        UnblockDNSPort_button.setToolTip('Enables all ports through which DNS traffic flows.')
        UnblockDNSPort_button.clicked.connect(self.run_unblockDNSPort_script)
        layout.addWidget(UnblockDNSPort_button)

        UnblockDNSProtocol_button = QPushButton('Unblock DNS Protocol')
        UnblockDNSProtocol_button.setToolTip('Enables flow of Packets using DNS protocol.')
        UnblockDNSProtocol_button.clicked.connect(self.run_unblockDNSProtocol_script)
        layout.addWidget(UnblockDNSProtocol_button)

        self.result_label = QLabel('')  # Label to display the result of the executed scripts
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def run_script(self, command):
        full_command = f"{getRedis(11)} '{command}'"

        process = subprocess.Popen(full_command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Ensure sudo_password is a string
        sudo_password = str(self.sudo_password) + '\n'

        stdout, stderr = process.communicate(input=sudo_password)

        if process.returncode == 0:
            self.result_label.setText(stdout)
        else:
            self.result_label.setText(f"Error: {stderr}")


    def run_blockDNSport_script(self):
        self.run_script(getRedis(12))
        with open('script.sh', 'a') as file:
            # Write content to the file
            file.write(f"{getRedis(12)}\n")

    def run_blockDNSprotocol_script(self):
        self.run_script(getRedis(13))
        with open('script.sh', 'a') as file:
            # Write content to the file
            file.write(f"{getRedis(13)}\n")

    def run_unblockDNSPort_script(self):
        self.run_script(getRedis(14))
        with open('script.sh', 'a') as file:
            # Write content to the file
            file.write(f"{getRedis(14)}\n")

    def run_unblockDNSProtocol_script(self):
        self.run_script(getRedis(15))
        with open('script.sh', 'a') as file:
            # Write content to the file
            file.write(f"{getRedis(15)}\n")