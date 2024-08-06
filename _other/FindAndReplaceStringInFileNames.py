import sys
import os
import pkg_resources

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
        print('opening file dialog')
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.directory_input.setText(directory)
    
    def rename_files(self):
        print('setting vars')
        directory = self.directory_input.text()
        old_string = self.old_string_input.text()
        new_string = self.new_string_input.text()
        print('set vars')
        
        if not directory or not old_string:
            return  # Add your preferred error handling here
        
        print('running fuction')
        self.process_directory(directory, old_string, new_string)
    
    def process_directory(self, directory, old_string, new_string):
        print('runnning prcoess directory')
        for filename in os.listdir(directory):
            if old_string in filename:
                if new_string == "":
                    # Remove old_string from filename
                    new_filename = filename.replace(old_string, "")
                else:
                    # Replace old_string with new_string
                    print('runnning variable rename')
                    new_filename = filename.replace(old_string, new_string)
                
                old_filepath = os.path.join(directory, filename)
                new_filepath = os.path.join(directory, new_filename)
                
                # Rename the file if the new filename is different from the old filename
                print('running rename')
                if old_filepath != new_filepath:
                    os.rename(old_filepath, new_filepath)
                    print(f'Renamed: {filename} -> {new_filename}')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RenameFilesApp()
    window.show()
    sys.exit(app.exec_())
