import subprocess
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel

class CupsRemovalApp(QWidget):
    def init_ui(self):
        layout = QVBoxLayout()

        check_button = QPushButton('Check and Remove CUPS')
        check_button.clicked.connect(self.check_and_remove_cups)
        layout.addWidget(check_button)

        self.result_label = QLabel()
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def check_and_remove_cups(self):
        result = subprocess.run(['dpkg-query', '-W', '-f=${db:Status-Status}', 'cups'], capture_output=True, text=True)

        if result.stdout.strip() == 'installed':
            self.result_label.setText("CUPS is installed. Removing CUPS...")
            subprocess.run(['sudo', 'apt', 'purge', 'cups'])
            self.result_label.setText("CUPS has been removed.")
        else:
            self.result_label.setText("CUPS is not installed. No action needed.")
