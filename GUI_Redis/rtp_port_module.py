from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSizePolicy
import subprocess
from RedisCache_module import getRedis
class BlockRTPModule(QWidget):
    def __init__(self, sudo_password):
        super(BlockRTPModule, self).__init__()

        self.sudo_password = sudo_password

        layout = QVBoxLayout()
        intro_label = QLabel(
            "Prevents Real-time Transport Protocol (RTP) traffic, enhancing security by controlling audio and video communication.")
        intro_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        intro_label.setWordWrap(True)
        layout.addWidget(intro_label)

        blockRTPPort_button = QPushButton('Block RTP Port')
        blockRTPPort_button.clicked.connect(self.run_blockRTPport_script)
        layout.addWidget(blockRTPPort_button)

        UnblockRTPPort_button = QPushButton('Unblock RTP Port')
        UnblockRTPPort_button.clicked.connect(self.run_unblockRTPport_script)
        layout.addWidget(UnblockRTPPort_button)

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

    def run_blockRTPport_script(self):
        self.run_script({getRedis(61)})
        with open('script.sh', 'a') as file:
            # Write content to the file
            file.write(f"{getRedis(61)}'\n")
    def run_unblockRTPport_script(self):
        self.run_script({getRedis(62)})
        with open('script.sh', 'a') as file:
            # Write content to the file
            file.write(f"{getRedis(62)}'\n")