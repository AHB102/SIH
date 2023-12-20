from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QCheckBox, QPlainTextEdit, QLabel, QSizePolicy
from PyQt5.QtGui import QTextCharFormat, QColor
from PyQt5.QtCore import Qt
import subprocess

class FirewallManagementModule(QWidget):
    def __init__(self, sudo_password):
        super(FirewallManagementModule, self).__init__()

        self.sudo_password = sudo_password

        layout = QVBoxLayout()
        intro_label = QLabel("Controls incoming and outgoing network traffic based on a set of rules, enhancing network security.")
        intro_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        intro_label.setWordWrap(True)
        layout.addWidget(intro_label)

        enable_button = QPushButton('Enable Firewall')
        enable_button.clicked.connect(self.enable_firewall)
        layout.addWidget(enable_button)

        disable_button = QPushButton('Disable Firewall')
        disable_button.clicked.connect(self.disable_firewall)
        layout.addWidget(disable_button)

        status_button = QPushButton('Check Firewall Status')
        status_button.clicked.connect(self.check_firewall_status)
        layout.addWidget(status_button)

        # Result textbox for displaying firewall status
        self.result_textbox = QPlainTextEdit()
        self.result_textbox.setReadOnly(True)

        # Set text color to blue
        char_format = QTextCharFormat()
        char_format.setForeground(Qt.blue)
        self.result_textbox.setCurrentCharFormat(char_format)

        layout.addWidget(self.result_textbox)

        # Checkboxes for specific firewall rules
        self.checkboxes = {
            'AllowIncoming': QCheckBox('Allow Incoming'),
            'AllowOutgoing': QCheckBox('Allow Outgoing'),
            'AllowSSH': QCheckBox('Allow SSH'),
            'AllowHTTP': QCheckBox('Allow HTTP'),
            'AllowHTTPS': QCheckBox('Allow HTTPS'),
            'AllowOpenVPN': QCheckBox('Allow OpenVPN'),
        }

        for checkbox in self.checkboxes.values():
            checkbox.setStyleSheet('QCheckBox { color: blue; }'
                                   'QCheckBox::indicator { background-color: white; border: 1px solid black; }'  # Set border
                                   'QCheckBox:checked { background-color: lightblue; }')  # Set background color for checked state
            layout.addWidget(checkbox)

        # Apply button
        self.apply_button = QPushButton('Apply Rules')
        self.apply_button.clicked.connect(self.apply_firewall_rules)
        layout.addWidget(self.apply_button)

        self.setLayout(layout)

    def set_apply_button_state(self, enabled):
        self.apply_button.setEnabled(enabled)

    def run_script(self, command):
        full_command = f"echo {self.sudo_password} | sudo -S {command}\n"
        result = subprocess.run(full_command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            self.result_textbox.appendPlainText(result.stdout)
        else:
            error_message = f"Error ({result.returncode}): {result.stderr}"
            self.result_textbox.appendPlainText(error_message)

    def enable_firewall(self):
        enable_command = "sudo ufw enable"
        with open('script.sh', 'a') as file:
            # Write content to the file
            file.write(f"{enable_command}\n")
        self.run_script(enable_command)
        self.set_apply_button_state(True)  # Enable the "Apply Rules" button

    def disable_firewall(self):
        disable_command = "sudo ufw disable"
        with open('script.sh', 'a') as file:
            # Write content to the file
            file.write(f"{disable_command}\n")
        self.run_script(disable_command)
        self.set_apply_button_state(False)  # Disable the "Apply Rules" button

    def check_firewall_status(self):
        status_command = "sudo ufw status"
        with open('script.sh', 'a') as file:
            # Write content to the file
            file.write(f"{status_command}\n")
        self.run_script(status_command)

        # Check the status of each checkbox based on the current rules
        for checkbox in self.checkboxes.values():
            checkbox.setChecked(self.check_firewall_rule_status(checkbox.objectName()))

    def apply_firewall_rules(self):
        # Execute allow/deny scripts based on checkbox state
        if self.checkboxes['AllowIncoming'].isChecked():
            self.run_script("sudo ufw default allow incoming")
            with open('script.sh', 'a') as file:
                # Write content to the file
                file.write(f"sudo ufw default allow incoming\n")
        else:
            self.run_script("sudo ufw default deny incoming")
            with open('script.sh', 'a') as file:
                # Write content to the file
                file.write(f"sudo ufw default deny incoming\n")

        if self.checkboxes['AllowOutgoing'].isChecked():
            self.run_script("sudo ufw default allow outgoing")
            with open('script.sh', 'a') as file:
                # Write content to the file
                file.write(f"sudo ufw default allow outgoing\n")
        else:
            self.run_script("sudo ufw default deny outgoing")
            with open('script.sh', 'a') as file:
                # Write content to the file
                file.write(f"sudo ufw default deny outgoing\n")

        if self.checkboxes['AllowSSH'].isChecked():
            self.run_script("sudo ufw allow ssh")
            with open('script.sh', 'a') as file:
                # Write content to the file
                file.write(f"sudo ufw allow ssh\n")
        else:
            self.run_script("sudo ufw deny ssh")
            with open('script.sh', 'a') as file:
                # Write content to the file
                file.write(f"sudo ufw deny ssh\n")

        if self.checkboxes['AllowHTTP'].isChecked():
            self.run_script("sudo ufw allow http")
            with open('script.sh', 'a') as file:
                # Write content to the file
                file.write(f"sudo ufw allow http\n")
        else:
            self.run_script("sudo ufw deny http")
            with open('script.sh', 'a') as file:
                # Write content to the file
                file.write(f"sudo ufw deny http\n")

        if self.checkboxes['AllowHTTPS'].isChecked():
            self.run_script("sudo ufw allow https")
        else:
            self.run_script("sudo ufw deny https")

        if self.checkboxes['AllowOpenVPN'].isChecked():
            self.run_script("sudo ufw allow openvpn")
        else:
            self.run_script("sudo ufw deny openvpn")

        # Refresh the firewall status
        self.check_firewall_status()

    def check_firewall_rule_status(self, rule_name):
        # Implement logic to check the status of specific firewall rules
        # Return True if the rule is enabled, False otherwise
        return False
