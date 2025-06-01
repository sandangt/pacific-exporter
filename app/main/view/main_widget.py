from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog

from app.main.dto import SubmitEventInfo


class MainWidget(QWidget):

    __NO_DIR_SELECTED_LABEL = 'No directory selected'

    submit_event = Signal(SubmitEventInfo)

    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        #region Input dir row
        input_layout = QHBoxLayout()
        self.__c_input_file_path = QLabel(self.__NO_DIR_SELECTED_LABEL)
        self.__c_input_file_path.setMinimumWidth(300)
        self.__c_input_file_path.setStyleSheet('border: 1px solid gray; padding: 4px;')
        self.__c_input_file_path.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        input_button = QPushButton('Input directory')
        input_button.clicked.connect(lambda _: self.__eh_on_open_directory_dialog(self.__c_input_file_path))
        input_layout.addWidget(self.__c_input_file_path)
        input_layout.addWidget(input_button)
        main_layout.addLayout(input_layout)
        #endregion

        #region Output dir row
        output_layout = QHBoxLayout()
        self.__c_output_file_path = QLabel(self.__NO_DIR_SELECTED_LABEL)
        self.__c_output_file_path.setMinimumWidth(300)
        self.__c_output_file_path.setStyleSheet('border: 1px solid gray; padding: 4px;')
        self.__c_output_file_path.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        output_button = QPushButton('Output directory')
        output_button.clicked.connect(lambda _: self.__eh_on_open_directory_dialog(self.__c_output_file_path))
        output_layout.addWidget(self.__c_output_file_path)
        output_layout.addWidget(output_button)
        main_layout.addLayout(output_layout)
        #endregion

        #region Submit button
        self.start_button = QPushButton('Start')
        self.start_button.setMinimumHeight(40)
        self.start_button.clicked.connect(self.__eh_on_submit)
        main_layout.addWidget(self.start_button, alignment=Qt.AlignmentFlag.AlignCenter)
        #endregion

        #region Status label
        self.__c_status_label = QLabel('')
        self.__c_status_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.__c_status_label.setStyleSheet('color: white; background-color: black; padding: 4px;')
        self.__c_status_label.hide()
        main_layout.addWidget(self.__c_status_label)
        #endregion

    def __eh_on_open_directory_dialog(self, file_path_component: QLabel):
        if directory := QFileDialog.getExistingDirectory(
            self, 'Select Directory', '', QFileDialog.Option.ShowDirsOnly
        ):
            file_path_component.setText(directory)
            self.__c_status_label.hide()

    def __eh_on_submit(self):
        input_dir = self.__c_input_file_path.text().strip()
        output_dir = self.__c_output_file_path.text().strip()

        result = SubmitEventInfo(input_dir=input_dir,
                                 output_dir=output_dir)

        if not input_dir or input_dir == self.__NO_DIR_SELECTED_LABEL:
            result.ready_to_start = False
            result.err_msg = 'Please select input directory'
            self.submit_event.emit(result)
            return

        if not output_dir or output_dir == self.__NO_DIR_SELECTED_LABEL:
            result.ready_to_start = False
            result.err_msg = 'Please select output directory'
            self.submit_event.emit(result)
            return

        result.ready_to_start = True
        self.submit_event.emit(result)

    def set_status(self, msg: str):
        self.__c_status_label.setText(msg)
        self.__c_status_label.show()
