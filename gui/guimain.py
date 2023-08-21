
import functools
from PyQt6.QtWidgets import *
from .callbacks import *



class MW(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def url_changed(self):
        self.btn_dl.setEnabled(False)

    def initUI(self):
        self.setWindowTitle("ncmget")
        self.resize(420, 170)

        self.edit = QLineEdit(self)
        self.edit.setGeometry(10, 15, 400, 40)
        self.edit.setPlaceholderText("URL/SongID")
        self.edit.textChanged.connect(self.url_changed)

        self.status_bar = QLineEdit(self)
        self.status_bar.setGeometry(10, 65, 400, 25)
        self.status_bar.setText("-")
        self.status_bar.setEnabled(False)
        
        self.btn_inf = QPushButton("获取信息", self)
        self.btn_inf.setGeometry(230, 110, 80, 40)
        self.btn_inf.pressed.connect(functools.partial(ui_get_song_information_async, self))

        self.btn_dl = QPushButton("下载", self)
        self.btn_dl.setGeometry(320, 110, 80, 40)
        self.btn_dl.pressed.connect(functools.partial(ui_download_async, self))
        self.btn_dl.setEnabled(False)

        self.label_engine = QLabel(self)
        self.label_engine.setGeometry(20, 120, 80, 20)
        self.label_engine.setText("webdriver")

        self.combobox_engine = QComboBox(self)
        self.combobox_engine.addItems(["Chrome", "Firefox"])
        self.combobox_engine.setGeometry(85, 120, 80, 20)

        self.show()