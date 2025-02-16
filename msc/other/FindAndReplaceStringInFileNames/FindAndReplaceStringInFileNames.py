import sys
import os
import subprocess
import pkg_resources

# Function to check and install PyQt5 if not already installed
def install_package(package_name):
    try:
        pkg_resources.get_distribution(package_name)
    except pkg_resources.DistributionNotFound:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name])

# Check if PyQt5 is installed; if not, install it
install_package('PyQt5')

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QWidget, QFileDialog, QLabel

class RenameFilesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("File Renamer")
        self.setGeometry(100, 100, 400, 200)
        
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        
        self.directory_label = QLabel("Select directory:")
        layout.addWidget(self.directory_label)
        
        self.directory_input = QLineEdit()
        layout.addWidget(self.directory_input)
        
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.browse_button)
        
        self.old_string_label = QLabel("String to replace:")
        layout.addWidget(self.old_string_label)
        
        self.old_string_input = QLineEdit()
        layout.addWidget(self.old_string_input)
        
        self.new_string_label = QLabel("Replacement string (leave empty to remove):")
        layout.addWidget(self.new_string_label)
        
        self.new_string_input = QLineEdit()
        layout.addWidget(self.new_string_input)
        
        self.rename_button = QPushButton("Rename Files")
        self.rename_button.clicked.connect(self.rename_files)
        layout.addWidget(self.rename_button)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    
    def open_file_dialog(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.directory_input.setText(directory)
    
    def rename_files(self):
        directory = self.directory_input.text()
        old_string = self.old_string_input.text()
        new_string = self.new_string_input.text()
        
        if not directory or not old_string:
            return  # Add your preferred error handling here
        
        self.process_directory(directory, old_string, new_string)
    
    def process_directory(self, directory, old_string, new_string):
        for filename in os.listdir(directory):
            if old_string in filename:
                if new_string == "":
                    # Remove old_string from filename
                    new_filename = filename.replace(old_string, "")
                else:
                    # Replace old_string with new_string
                    new_filename = filename.replace(old_string, new_string)
                
                old_filepath = os.path.join(directory, filename)
                new_filepath = os.path.join(directory, new_filename)
                
                # Rename the file if the new filename is different from the old filename
                if old_filepath != new_filepath:
                    os.rename(old_filepath, new_filepath)
                    print(f'Renamed: {filename} -> {new_filename}')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RenameFilesApp()
    window.show()
    sys.exit(app.exec_())
