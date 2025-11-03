from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QWidget, QMessageBox, QProgressDialog, QFileDialog
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl, QTimer, Qt, QTime
from pydub import AudioSegment
from Designer.ClipEditorWidget import Ui_clipEditorWidget
import math, os, shutil

class ClipEditorWidget(QWidget, Ui_clipEditorWidget):
    def __init__(self, songList: list[str]):
        super().__init__()
        self.setupUi(self)

        self.folderPath = "Data/Temp"

        self.songList = songList
        self.index = 0

        self.seconds = 0
        self.minutes = 0

        self.Timer = QTimer()
        self.Timer.setInterval(1000)

        self.Timer.timeout.connect(self.setSliderValue)

        self.playStatus = False

        self.startTime = QTime(0, 0, 0)
        self.endTime   = QTime(0, 0, 0)
        self.volume  = 0.0
        self.fadein  = 0.0
        self.fadeout = 0.0

        self.loadingDialog = None

        self.mediaPlayer = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.mediaPlayer.setAudioOutput(self.audioOutput)

        self.initUi()
        self.reset()


    def initUi(self):
        self.volumeSlider.setRange(-60, 20)
        self.volumeSpinBox.setRange(-60.0, 20.0)
        self.volumeSpinBox.setDecimals(1)

        self.fadeinSlider.setRange(0, 100)
        self.fadeinSpinBox.setRange(0.0, 100.0)
        self.fadeinSpinBox.setDecimals(1)

        self.fadeoutSlider.setRange(0, 100)
        self.fadeoutSpinBox.setRange(0.0, 100.0)
        self.fadeoutSpinBox.setDecimals(1)

        self.startTimeEdit.setDisplayFormat("mm:ss")
        self.endTimeEdit.setDisplayFormat("mm:ss")

        self.volumeSlider.valueChanged.connect(lambda v: self.volumeSpinBox.setValue(v*0.1))
        self.volumeSpinBox.valueChanged.connect(lambda v: self.volumeSlider.setValue(int(v*10)))

        self.fadeinSlider.valueChanged.connect(lambda v: self.fadeinSpinBox.setValue(v*0.1))
        self.fadeinSpinBox.valueChanged.connect(lambda v: self.fadeinSlider.setValue(int(v*10)))

        self.fadeoutSlider.valueChanged.connect(lambda v: self.fadeoutSpinBox.setValue(v*0.1))
        self.fadeoutSpinBox.valueChanged.connect(lambda v: self.fadeoutSlider.setValue(int(v*10)))

        self.progressSlider.sliderMoved.connect(self.sliderProgressMoved)
        self.progressSlider.sliderReleased.connect(self.sliderProgressReleased)

        self.playButton.clicked.connect(self.playButtonClicked)
        self.prevButton.clicked.connect(self.prevButtonClicked)
        self.nextButton.clicked.connect(self.nextButtonClicked)
        self.resetButton.clicked.connect(self.resetButtonClicked)
        self.trailorButton.clicked.connect(self.trailorButtonClicked)

        self.mediaPlayer.mediaStatusChanged.connect(self.progressInit)


    def loadSong(self):
        self.loadingDialog = QProgressDialog("正在加载音频...", None, 0, 0, self)
        self.loadingDialog.setWindowTitle("请稍候")
        self.loadingDialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.loadingDialog.show()

        self.mediaPlayer.setSource(QUrl.fromLocalFile(os.path.join(os.path.abspath(self.folderPath), self.songList[self.index])))
        self.songNameLabel.setText(f"{self.index+1}. {self.songList[self.index].split('/')[-1]}")

    def loadTrailor(self):
        self.loadingDialog = QProgressDialog("正在加载预览音频...", None, 0, 0, self)
        self.loadingDialog.setWindowTitle("请稍候")
        self.loadingDialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.loadingDialog.show()

        self.mediaPlayer.setSource(QUrl.fromLocalFile(os.path.join(os.path.abspath(self.folderPath),  f"trailor_{self.songList[self.index]}")))
        self.songNameLabel.setText(f"{self.index+1}. {self.songList[self.index].split('/')[-1]}")


    def progressInit(self, status):

        if status == QMediaPlayer.MediaStatus.LoadedMedia:

            self.seconds = self.mediaPlayer.duration() // 1000

            self.minutes = self.seconds // 60

            self.progressSlider.setRange(0, self.seconds)

            mins = self.minutes
            secs = self.seconds % 60

            self.endTime = QTime(0, mins, secs)
            self.endTimeEdit.setTime(self.endTime)
            self.endTimeEdit.setMaximumTime(self.endTime)

            self.startTime = QTime(0, 0, 0)
            self.startTimeEdit.setTime(self.startTime)
            self.startTimeEdit.setMaximumTime(self.endTime)


            self.playTimeLabel.setText("%d:%02d" % (mins, secs))
            self.endTimeLabel.setText("%d:%02d" % (mins, secs))

            if hasattr(self, "loadingDialog"):
                self.loadingDialog.close()


    def reset(self):
        self.volumeSlider.setValue(0)
        self.volumeSpinBox.setValue(0.0)
        self.fadeinSlider.setValue(0)
        self.fadeinSpinBox.setValue(0.0)
        self.fadeoutSlider.setValue(0)
        self.fadeoutSpinBox.setValue(0.0)

        self.progressSlider.setValue(0)
        self.playTimeLabel.setText("0:00")
        self.endTimeLabel.setText("0:00")
        self.playButton.setText("播放")

        self.loadSong()

        self.Timer.start()

        if self.index == len(self.songList) - 1:
            self.nextButton.setText("导出")
            self.nextButton.clicked.disconnect()
            self.nextButton.clicked.connect(self.exportButtonClicked)
        else:
            self.nextButton.setText("下一首")
            self.nextButton.clicked.disconnect()
            self.nextButton.clicked.connect(self.nextButtonClicked)

        self.playButton.setText("暂停")


    def setSliderValue(self):

        self.progressSlider.setValue(self.mediaPlayer.position() // 1000)

        curtSecs = self.mediaPlayer.position() // 1000
        curtMins = curtSecs // 60
        curtSecs = curtSecs % 60

        self.playTimeLabel.setText("%d:%02d" % (curtMins, curtSecs))


    def sliderProgressMoved(self):
        self.Timer.stop()

        pos = self.progressSlider.value() * 1000

        self.mediaPlayer.setPosition(pos)

        crtSecs = self.mediaPlayer.position() // 1000
        crtMins = crtSecs // 60
        crtSecs = crtSecs % 60

        self.playTimeLabel.setText("%d:%02d" % (crtMins, crtSecs))


    def sliderProgressReleased(self):
        self.Timer.start()


    def prevButtonClicked(self):
        if self.index == 0:
            QMessageBox.warning(self, "提示", "已经是第一首歌曲")
            return

        self.index -= 1
        self.reset()


    def resetButtonClicked(self):
        self.loadSong()


    def playButtonClicked(self):
        if not self.playStatus:
            self.mediaPlayer.play()
            self.playButton.setText("暂停")
            self.playStatus = True
        else:
            self.mediaPlayer.pause()
            self.playButton.setText("播放")
            self.playStatus = False


    def trailorButtonClicked(self):
        self.startTime = self.startTimeEdit.time()
        self.endTime = self.endTimeEdit.time()
        self.volume = self.volumeSpinBox.value()
        self.fadein = self.fadeinSpinBox.value()
        self.fadeout = self.fadeoutSpinBox.value()
        startTime = self.startTime.minute()*60 + self.startTime.second()
        endTime   = self.endTime.minute()*60 + self.endTime.second()

        if endTime <= startTime:
            QMessageBox.warning(self, "提示", "结束时间必须大于开始时间")
            return

        audio = AudioSegment.from_file(os.path.join(os.path.abspath(self.folderPath), self.songList[self.index]))
        audio = audio[startTime*1000 : endTime*1000]
        audio = audio.apply_gain(self.volume)
        if self.fadein != 0.0:
            audio = audio.fade_in(int(self.fadein*1000))
        if self.fadeout != 0.0:
            audio = audio.fade_out(int(self.fadeout*1000))
        trailor = os.path.join(os.path.abspath(self.folderPath), f"trailor_{self.songList[self.index]}")
        audio.export(trailor, format="mp3")

        QMessageBox.information(self, "提示", "预览音频已生成")

        self.loadTrailor()

    def nextButtonClicked(self):
        if self.index == len(self.songList) - 1:
            QMessageBox.warning(self, "提示", "已经是最后一首歌曲")
            return
        self.index += 1
        self.reset()


    def exportButtonClicked(self):
        combined = AudioSegment.empty()

        for file in self.songList:
            filePath = os.path.join(os.path.abspath(self.folderPath), f"trailor_{file}")
            seg = AudioSegment.from_file(filePath, format="mp3")
            combined += seg

        filePath, _ = QFileDialog.getSaveFileName(
            self,
            "选择输出文件",
            "output.mp3",  # 默认文件名
            "音频文件 (*.mp3)"
        )

        if filePath:  # 用户点了保存
            try:
                # 导出音频
                combined.export(filePath, format="mp3")
                QMessageBox.information(self, "成功", f"已导出到 {filePath}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导出失败: {e}")

