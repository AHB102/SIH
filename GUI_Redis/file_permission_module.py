from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QSizePolicy
import subprocess
from RedisCache_module import getRedis
class FilePermissionModule(QWidget):
    def __init__(self, sudo_password):
        super(FilePermissionModule, self).__init__()

        self.sudo_password = sudo_password

        layout = QVBoxLayout()
        intro_label = QLabel(
            "Controls access to files and directories, specifying who can read, write, or execute them, enhancing data security.")
        intro_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        intro_label.setWordWrap(True)
        layout.addWidget(intro_label)
        read_button = QPushButton('Read Only')
        read_button.clicked.connect(self.run_read_script)
        layout.addWidget(read_button)

        write_button = QPushButton('Write Only')
        write_button.clicked.connect(self.run_write_script)
        layout.addWidget(write_button)

        execute_button = QPushButton('Execute Only')
        execute_button.clicked.connect(self.run_execute_script)
        layout.addWidget(execute_button)

        no_permission_button = QPushButton('No Permission')
        no_permission_button.clicked.connect(self.run_no_permission_script)
        layout.addWidget(no_permission_button)

        self.result_label = QLabel('')  # Label to display the result of the executed scripts
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def run_script(self, command):
        full_command = f"{getRedis(1)} {self.sudo_password} | {getRedis(2)} {command}"
        with open('script.sh', 'a') as file:
            # Write content to the file
            file.write(f"sudo {command}\n")
        result = subprocess.run(full_command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            self.result_label.setText(result.stdout)
        else:
            self.result_label.setText(f"Error: {result.stderr}")

    def run_read_script(self):
        filename = self.get_file_name()
        self.run_script(f'{getRedis(22)} "{filename}"')

    def run_write_script(self):
        filename = self.get_file_name()
        self.run_script(f'{getRedis(23)} "{filename}"')

    def run_execute_script(self):
        filename = self.get_file_name()
        self.run_script(f'{getRedis(24)} "{filename}"')

    def run_no_permission_script(self):
        filename = self.get_file_name()
        self.run_script(f'{getRedis(25)} "{filename}"')

    def get_file_name(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*);;Text Files (*.txt);;Python Files (*.py)")
        return filename
