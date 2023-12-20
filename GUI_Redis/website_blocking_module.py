from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QInputDialog, QMessageBox, QSizePolicy
from PyQt5.QtCore import QThread, pyqtSignal
import subprocess
from RedisCache_module import getRedis
class WebsiteBlockingModule(QWidget):
    def __init__(self, sudo_password):
        super(WebsiteBlockingModule, self).__init__()

        self.sudo_password = sudo_password

        layout = QVBoxLayout()
        intro_label = QLabel(
            "Restricts access to specified websites, enhancing security by controlling web content and potential threats")
        intro_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        intro_label.setWordWrap(True)
        layout.addWidget(intro_label)
        add_website_button = QPushButton('Add Website to Blocklist')
        add_website_button.setToolTip('Adds website to list of blocked websites.')
        add_website_button.clicked.connect(self.add_website_to_blocklist)
        layout.addWidget(add_website_button)

        self.result_label = QLabel('')  # Label to display the result of the executed scripts
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def run_script(self, command):
        full_command = f"{getRedis(1)} {self.sudo_password} | {getRedis(2)} {command}"
        result = subprocess.run(full_command, shell=True, capture_output=True, text=True)
        with open('script.sh', 'a') as file:
            # Write content to the file
            file.write(f"{full_command}\n")
        if result.returncode == 0:
            self.result_label.setText(result.stdout)
        else:
            self.result_label.setText(f"Error: {result.stderr}")

    def add_website_to_blocklist(self):
        # Input dialog to get the website to block
        website, ok = QInputDialog.getText(self, 'Website Blocking', 'Enter Website to Block:')
        if ok and website:
            # Add a wildcard for subdomains
            block_entry = f'127.0.0.1 {website} www.{website} *.{website}'
            self.run_script(f"{getRedis(1)} '{block_entry}' | {getRedis(10)}")

            self.result_label.setText(f"Website {website} and its subdomains added to blocklist.")
        elif not website and not ok:
            # User pressed Cancel
            pass
        else:
            QMessageBox.warning(self, 'Website Blocking', 'Please enter a website to block.')

# Example usage:
# sudo_password = "your_sudo_password"
# website_blocking_module = WebsiteBlockingModule(sudo_password)
# website_blocking_module.show()
