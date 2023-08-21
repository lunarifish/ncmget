
from PyQt6.QtCore import QThread
from network_ import get_song_information, build_url, download
import time



class ui_get_song_information(QThread):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def run(self):
        self.app.btn_inf.setEnabled(False)
        self.app.status_bar.setText("获取歌曲信息..")

        input_text = str(self.app.edit.text())
        if (song_url := build_url(input_text, False)) is not None:
            if (song_information := get_song_information(song_url, self.app.combobox_engine.currentText())) != "":
                song_information = song_information.replace("/", ", ")
                self.app.status_bar.setText(song_information)
                self.app.btn_dl.setEnabled(True)
            else:
                self.app.status_bar.setText("获取失败")
        else:
            self.app.status_bar.setText("输入不合法")

        self.app.btn_inf.setEnabled(True)


def ui_get_song_information_async(app):
    t = ui_get_song_information(app)
    t.start()
    t.exec()



class ui_download(QThread):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def run(self):
        self.app.btn_dl.setEnabled(False)
        self.app.btn_dl.setText("下载中")

        input_text = str(self.app.edit.text())
        outer_url = build_url(input_text, True)
        print("source:    ", build_url(input_text, False))
        print("redirect:  ", outer_url)
        print("fetching")

        download(outer_url, self.app.status_bar.text() + ".mp3")

        self.app.btn_dl.setEnabled(True)
        self.app.btn_dl.setText("下载成功")
        time.sleep(5)
        self.app.btn_dl.setText("下载")


def ui_download_async(app):
    t = ui_download(app)
    t.start()
    t.exec()
