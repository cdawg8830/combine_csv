from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QLineEdit, QProgressBar, QTextEdit, QFileDialog, QHBoxLayout
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor
import sys
import os
from csv_merger_app.core.csv_merger import CSVMerger

class FileDropLabel(QLabel):
    files_dropped = pyqtSignal(list)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptDrops(True)
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    def dropEvent(self, event):
        files = []
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path.endswith('.csv'):
                files.append(path)
        if files:
            self.files_dropped.emit(files)

class MergeThread(QThread):
    finished = pyqtSignal(bool, str)
    def __init__(self, file_paths, output_path):
        super().__init__()
        self.file_paths = file_paths
        self.output_path = output_path
    def run(self):
        success, error_report = CSVMerger.merge_files(self.file_paths, self.output_path)
        self.finished.emit(success, error_report)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Combine CSV")
        self.setMinimumSize(650, 700)
        font = QFont("San Francisco", 11)
        self.setFont(font)
        # Set dark palette for the app
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(35, 39, 46))
        dark_palette.setColor(QPalette.WindowText, QColor(245, 246, 250))
        dark_palette.setColor(QPalette.Base, QColor(35, 39, 46))
        dark_palette.setColor(QPalette.AlternateBase, QColor(45, 49, 58))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(245, 246, 250))
        dark_palette.setColor(QPalette.ToolTipText, QColor(35, 39, 46))
        dark_palette.setColor(QPalette.Text, QColor(245, 246, 250))
        dark_palette.setColor(QPalette.Button, QColor(45, 49, 58))
        dark_palette.setColor(QPalette.ButtonText, QColor(245, 246, 250))
        dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        dark_palette.setColor(QPalette.Highlight, QColor(79, 140, 255))
        dark_palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        QApplication.instance().setPalette(dark_palette)
        # Apply dark theme stylesheet
        self.setStyleSheet('''
            QWidget { background: #23272e; color: #f5f6fa; }
            QLabel, QLineEdit, QTextEdit, QListWidget, QPushButton {
                color: #f5f6fa;
                background: #23272e;
            }
            QLineEdit, QTextEdit, QListWidget {
                border: 1px solid #444a57;
                border-radius: 6px;
                padding: 6px;
                background: #23272e;
                color: #f5f6fa;
            }
            QLineEdit:disabled, QTextEdit:disabled, QListWidget:disabled {
                background: #23272e;
                color: #888;
            }
            QLineEdit::placeholder, QTextEdit::placeholder {
                color: #b0b3b8;
            }
            QPushButton {
                background: #2d313a;
                border: 1px solid #444a57;
                border-radius: 6px;
                padding: 8px 16px;
            }
            QPushButton:disabled {
                background: #23272e;
                color: #888;
            }
            QPushButton:hover:!disabled {
                background: #3a3f4b;
            }
            QProgressBar {
                background: #2d313a;
                border-radius: 4px;
            }
            QProgressBar::chunk {
                background-color: #4f8cff;
                border-radius: 4px;
            }
            QScrollBar:vertical, QScrollBar:horizontal {
                background: #23272e;
            }
        ''')
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Header
        header = QLabel("<h1 style='font-size:2em;'>CSV Merger</h1><p style='font-size:1.1em;'>Drag and drop CSV files or click to select files to merge</p>")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        # Drag-and-drop area
        self.drop_area = FileDropLabel("Drop CSV files here or click to browse")
        self.drop_area.setStyleSheet("""
            border: 2px dashed #aaa;
            border-radius: 12px;
            padding: 48px;
            text-align: center;
            background: #23272e;
            font-size: 1.1em;
            color: #f5f6fa;
        """)
        self.drop_area.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.drop_area)
        self.drop_area.mousePressEvent = self.open_file_dialog
        self.drop_area.files_dropped.connect(self.add_files)

        # File list + Clear All button
        file_list_layout = QHBoxLayout()
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.ExtendedSelection)
        self.file_list.setMinimumHeight(120)
        file_list_layout.addWidget(self.file_list)
        self.clear_btn = QPushButton("Clear All")
        self.clear_btn.clicked.connect(self.clear_file_list)
        file_list_layout.addWidget(self.clear_btn)
        layout.addLayout(file_list_layout)

        # Output filename input
        out_layout = QHBoxLayout()
        out_label = QLabel("Output Filename:")
        self.output_input = QLineEdit("merged_data.csv")
        self.output_input.setStyleSheet("background: #23272e; color: #f5f6fa;")
        out_layout.addWidget(out_label)
        out_layout.addWidget(self.output_input)
        layout.addLayout(out_layout)

        # Merge button
        self.merge_btn = QPushButton("Merge CSV Files")
        self.merge_btn.setMinimumHeight(36)
        layout.addWidget(self.merge_btn)

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        self.progress.setStyleSheet("QProgressBar { height: 8px; border-radius: 4px; background: #2d313a; } QProgressBar::chunk { background-color: #4f8cff; border-radius: 4px; }")
        layout.addWidget(self.progress)

        # Error reporting area
        self.error_area = QTextEdit()
        self.error_area.setReadOnly(True)
        self.error_area.setPlaceholderText("Error messages will appear here.")
        self.error_area.setMinimumHeight(100)
        self.error_area.setStyleSheet("background: #23272e; color: #f5f6fa; border-radius: 8px; padding: 8px;")
        layout.addWidget(self.error_area)

        # Connect signals
        self.merge_btn.clicked.connect(self.on_merge_clicked)
        self.merge_thread = None

    def open_file_dialog(self, event):
        files, _ = QFileDialog.getOpenFileNames(self, "Select CSV Files", "", "CSV Files (*.csv)")
        if files:
            self.add_files(files)

    def add_files(self, files):
        for f in files:
            if not any(self.file_list.item(i).text() == f for i in range(self.file_list.count())):
                self.file_list.addItem(f)

    def clear_file_list(self):
        self.file_list.clear()

    def on_merge_clicked(self):
        file_paths = [self.file_list.item(i).text() for i in range(self.file_list.count())]
        if not file_paths:
            self.error_area.setText("Please add at least one CSV file.")
            return
        output_name = self.output_input.text().strip()
        if not output_name:
            self.error_area.setText("Please enter an output filename.")
            return
        # Ask user for output location
        out_path, _ = QFileDialog.getSaveFileName(self, "Save Merged CSV As", output_name, "CSV Files (*.csv)")
        if not out_path:
            return
        # Disable UI
        self.set_ui_enabled(False)
        self.progress.setRange(0, 0)  # Indeterminate
        self.error_area.clear()
        # Start merge thread
        self.merge_thread = MergeThread(file_paths, out_path)
        self.merge_thread.finished.connect(self.on_merge_finished)
        self.merge_thread.start()

    def on_merge_finished(self, success, error_report):
        self.set_ui_enabled(True)
        self.progress.setRange(0, 100)
        self.progress.setValue(100 if success else 0)
        if success:
            self.error_area.setText("Merge complete!\n" + error_report)
        else:
            self.error_area.setText("Merge failed!\n" + error_report)

    def set_ui_enabled(self, enabled):
        self.merge_btn.setEnabled(enabled)
        self.file_list.setEnabled(enabled)
        self.output_input.setEnabled(enabled)
        self.drop_area.setEnabled(enabled)
        self.clear_btn.setEnabled(enabled)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_()) 