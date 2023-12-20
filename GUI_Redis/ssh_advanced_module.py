from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QDialog, QFormLayout, \
    QSizePolicy
import subprocess
from RedisCache_module import getRedis

class SSHAdvancedModule(QWidget):
    def __init__(self, sudo_password):
        super(SSHAdvancedModule, self).__init__()

        self.sudo_password = sudo_password

        layout = QVBoxLayout()
        intro_label = QLabel(
            "Implements advanced security measures for SSH, further protecting against unauthorized access and potential threats.")
        intro_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        intro_label.setWordWrap(True)
        layout.addWidget(intro_label)

        config_button = QPushButton('Configure SSH')
        config_button.clicked.connect(self.configure_ssh)
        layout.addWidget(config_button)

        key_auth_button = QPushButton('Setup SSH Key Authentication')
        key_auth_button.clicked.connect(self.setup_ssh_key_auth)
        layout.addWidget(key_auth_button)

        tcp_wrapper_button = QPushButton('Configure TCP Wrapper')
        tcp_wrapper_button.clicked.connect(self.configure_tcp_wrapper)
        layout.addWidget(tcp_wrapper_button)

        self.result_label = QLabel('')
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def run_script(self, command):
        full_command = f"{getRedis(11)} '{command}'"
        with open('script.sh', 'a') as file:
            # Write content to the file
            file.write(f"sudo bash -c {command}\n")
        process = subprocess.Popen(full_command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        sudo_password = str(self.sudo_password) + '\n'
        stdout, stderr = process.communicate(input=sudo_password)

        if process.returncode == 0:
            self.result_label.setText(stdout)
        else:
            self.result_label.setText(f"Error: {stderr}")

    def configure_ssh(self):
        ssh_config_dialog = SSHConfigDialog()
        result = ssh_config_dialog.exec_()
        if result == QDialog.Accepted:
            config_text = ssh_config_dialog.get_config_text()
            self.run_script(config_text)

    def setup_ssh_key_auth(self):
        self.run_script({getRedis(59)})

    def configure_tcp_wrapper(self):
        tcp_wrapper_dialog = TCPWrapperDialog()
        result = tcp_wrapper_dialog.exec_()
        if result == QDialog.Accepted:
            wrapper_text = tcp_wrapper_dialog.get_wrapper_text()
            self.run_script(wrapper_text)

class SSHConfigDialog(QDialog):
    def __init__(self):
        super(SSHConfigDialog, self).__init__()

        layout = QFormLayout()

        self.port_edit = QLineEdit()
        layout.addRow('Port:', self.port_edit)

        self.root_login_edit = QLineEdit()
        layout.addRow('PermitRootLogin:', self.root_login_edit)

        self.password_auth_edit = QLineEdit()
        layout.addRow('PasswordAuthentication:', self.password_auth_edit)

        self.allow_users_edit = QLineEdit()
        layout.addRow('AllowUsers:', self.allow_users_edit)

        self.setLayout(layout)

        self.button_box = QDialog.ButtonBox(QDialog.ButtonBox.Ok | QDialog.ButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout.addRow(self.button_box)

    def get_config_text(self):
        with open('script.sh', 'a') as file:
            # Write content to the file
            file.write(f"""
            {getRedis(64)} {self.port_edit.text()}/" {getRedis(60)}
            {getRedis(65)} {self.root_login_edit.text()}/" {getRedis(60)}
            {getRedis(66)} {self.password_auth_edit.text()}/" {getRedis(60)}
            {getRedis(67)} {self.allow_users_edit.text()}/" {getRedis(60)}
            {getRedis(63)}
            {getRedis(1)} "SSH configuration updated. Check /etc/ssh/sshd_config for the changes." 
            """)
        return f"""
            {getRedis(64)} {self.port_edit.text()}/" {getRedis(60)}
            {getRedis(65)} {self.root_login_edit.text()}/" {getRedis(60)}
            {getRedis(66)} {self.password_auth_edit.text()}/" {getRedis(60)}
            {getRedis(67)} {self.allow_users_edit.text()}/" {getRedis(60)}
            {getRedis(63)}
            {getRedis(1)} "SSH configuration updated. Check /etc/ssh/sshd_config for the changes."
        """

class TCPWrapperDialog(QDialog):
    def __init__(self):
        super(TCPWrapperDialog, self).__init__()

        layout = QVBoxLayout()

        self.hosts_edit = QTextEdit()
        layout.addWidget(self.hosts_edit)

        self.button_box = QDialog.ButtonBox(QDialog.ButtonBox.Ok | QDialog.ButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def get_wrapper_text(self):
        hosts = self.hosts_edit.toPlainText().strip()
        with open('script.sh', 'a') as file:
            # Write content to the file
            file.write(f"""
            {getRedis(1)} "sshd: {hosts}" | tee -a /etc/hosts.allow
            systemctl restart ssh
            {getRedis(1)} "TCP Wrapper configuration completed. Check /etc/hosts.allow for the changes."
        """)
        return f"""
            {getRedis(1)} "sshd: {hosts}" | tee -a /etc/hosts.allow
            systemctl restart ssh
            {getRedis(1)} "TCP Wrapper configuration completed. Check /etc/hosts.allow for the changes."
        """

# Example usage:
# sudo_password = "your_sudo_password"
# ssh_config_module = SSHAdvancedModule(sudo_password)
# ssh_config_module.show()
