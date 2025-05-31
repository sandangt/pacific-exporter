import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QHBoxLayout

from app.constant import XLSX_EXTENSION
from app.view.dto import ApplicationContext


class MainWindow(QMainWindow):
    __WINDOW_TITLE = 'Welcome to Pacific Exporter'
    __DEFAULT_LABEL = 'No directory selected'

    def __init__(self, app_ctx: ApplicationContext):
        self.__app_ctx = app_ctx
        super().__init__()
        self.__ui()

    def __ui(self):
        # region Window and main widget
        self.setWindowTitle(self.__WINDOW_TITLE)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        # endregion

        main_layout = QVBoxLayout()

        # Label (read-only display of selected directory)
        self.__c_file_path = QLabel(self.__DEFAULT_LABEL)
        self.__c_file_path.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__c_file_path.setWordWrap(True)
        main_layout.addWidget(self.__c_file_path)

        # Button to browse directory
        self.__c_browse_button = QPushButton('Select Directory')
        self.__c_browse_button.clicked.connect(self.__eh_on_open_directory_dialog)
        main_layout.addWidget(self.__c_browse_button)

        # Submit button
        self.__c_submit_button = QPushButton('Submit')
        self.__c_submit_button.clicked.connect(self.__eh_on_submit)
        main_layout.addWidget(self.__c_submit_button)

        central_widget.setLayout(main_layout)

    def __eh_on_open_directory_dialog(self):
        if directory := QFileDialog.getExistingDirectory(
            self, 'Select Directory', '', QFileDialog.Option.ShowDirsOnly
        ):
            self.__c_file_path.setText(directory)

    def __eh_on_submit(self):
        selected_directory = self.__c_file_path.text()
        if selected_directory and selected_directory != self.__DEFAULT_LABEL:
            self.__process()

    def __process(self):
        target_files = []
        for root, _, files in os.walk(self.__c_file_path.text()):
            target_files.extend([os.path.join(root, x) for x in files if x.endswith(XLSX_EXTENSION)])
        for file_path in target_files:
            self.__app_ctx.persist_service.import_workbook(file_path)
        self.__app_ctx.export_service.generate_report()
