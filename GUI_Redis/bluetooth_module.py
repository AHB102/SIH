from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSizePolicy
import subprocess
from RedisCache_module import getRedis
class BluetoothModule(QWidget):
    def __init__(self, sudo_password):
        super(BluetoothModule, self).__init__()

        self.sudo_password = sudo_password

        layout = QVBoxLayout()
        intro_label = QLabel("Disables Bluetooth connectivity to prevent unauthorized access and potential security risks.")
        intro_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        intro_label.setWordWrap(True)
        layout.addWidget(intro_label)

        disable_button = QPushButton('Disable Bluetooth')
        disable_button.setToolTip('Disables Bluetooth.')
        disable_button.clicked.connect(self.disable_bluetooth)
        layout.addWidget(disable_button)

        enable_button = QPushButton('Enable Bluetooth')
        enable_button.setToolTip('Enables Bluetooth.')
        enable_button.clicked.connect(self.enable_bluetooth)
        layout.addWidget(enable_button)

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

    def disable_bluetooth(self):
        # Disable Bluetooth service
        self.run_script(getRedis(16))
        # Prevent Bluetooth service from starting on boot
        self.run_script(getRedis(17))
        with open('script.sh', 'a') as file:
            # Write content to the file
            file.write(f"{getRedis(16)}\n")
            file.write(f"{getRedis(17)}\n")

    def enable_bluetooth(self):
        # Enable Bluetooth service
        self.run_script(getRedis(18))
        # Start Bluetooth service
        self.run_script(getRedis(19))
        with open('script.sh', 'a') as file:
            # Write content to the file
            file.write(f"{getRedis(18)}\n")
            file.write(f"{getRedis(19)}\n")
# Example usage:
# sudo_password = "your_password"
# bluetooth_module = BluetoothControlModule(sudo_password)
# bluetooth_module.show()
