import sys
from PyQt6.QtWidgets import QApplication
from src.UI.metaPage import MetaPage
from src.UI.GUI import MainWindow  

class AppController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = None
    def start_main_window(self, user_id):
        self.main_window = MainWindow(user_id)
        self.main_window.show()

    def run(self):
        meta = MetaPage(on_submit=self.start_main_window)
        meta.show()
        sys.exit(self.app.exec())

if __name__ == "__main__":
    controller = AppController()
    controller.run()