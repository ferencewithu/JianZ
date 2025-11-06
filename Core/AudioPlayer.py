from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtWidgets import QProgressDialog, QMessageBox


class AudioPlayer(QMediaPlayer):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.audioOutput = QAudioOutput()
        self.setAudioOutput(self.audioOutput)

        self.seconds = 0

        self.loadingDialog = QProgressDialog(None)

        self.mediaStatusChanged.connect(self.getDuration)


    def setVolumeLevel(self, level: float):
        """Set volume level in decibels."""
        linearVolume = 10 ** (level / 20)  # Convert dB to linear scale
        self.audioOutput.setVolume(linearVolume)


    def loadSource(self, src: str, audioType: str):
        """Load audio source from file path."""
        self.block(audioType)

        url = QtCore.QUrl.fromLocalFile(src)
        self.setSource(url)

    def getDuration(self):
        """Get duration of the loaded audio in milliseconds."""
        self.seconds = self.duration() // 1000

    def block(self, s : str):
        self.loadingDialog = QProgressDialog(f"正在加载{s}...", None, 0, 0, self)
        self.loadingDialog.setWindowTitle("请稍候")
        self.loadingDialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.loadingDialog.show()

