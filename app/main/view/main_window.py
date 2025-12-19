import os

from PySide6.QtWidgets import QMainWindow

from app.main.dto import ApplicationContext, SubmitEventInfo
from app.constant import XLSX_EXTENSION
from .main_widget import MainWidget


class MainWindow(QMainWindow):
    def __init__(self, app_ctx: ApplicationContext):
        self.__app_ctx = app_ctx
        super().__init__()
        self.__c_main_widget = MainWidget()
        self.setCentralWidget(self.__c_main_widget)
        self.resize(500, 300)
        self.__c_main_widget.submit_event.connect(self.__eh_on_submit)

    def __eh_on_submit(self, event_val: SubmitEventInfo):
        if not event_val.ready_to_start:
            self.__c_main_widget.set_status(event_val.err_msg)
            return

        try:
            self.__c_main_widget.set_status('Processing')
            self.__process(event_val.input_dir, event_val.output_dir)
            self.__c_main_widget.set_status('DONE')
        except Exception as ex:
            self.__c_main_widget.set_status('Cannot process due to error')
            print(ex)

    def __process(self, input_dir: str, output_dir: str):
        target_files = []
        for root, _, files in os.walk(input_dir):
            target_files.extend([os.path.join(root, x) for x in files if x.endswith(XLSX_EXTENSION)])
        for file_path in target_files:
            self.__app_ctx.persist_service.import_workbook(file_path)
        self.__app_ctx.export_service.generate_report(output_dir)
