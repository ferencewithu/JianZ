import os, shutil
import random
from PyQt6.QtWidgets import (
    QWidget, QLabel, QListWidget, QVBoxLayout,
    QListWidgetItem, QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt

from UI.ClipEditorWidget import ClipEditorWidget


class SongListWidget(QWidget):
    def __init__(self, folderPath: str, parent=None):
        super().__init__(parent)

        # ====== UI部件 ======
        self.titleLabel = QLabel("歌曲列表")
        self.numList = QListWidget()
        self.songList = QListWidget()
        self.shuffleButton = QPushButton("打乱顺序")
        self.editButton = QPushButton("进入剪辑")

        # ====== 其他对象 ======
        self.folderPath = folderPath
        self.songNames = []
        self.clipEditorWidget = None   # 改名以保持一致

        # ====== 初始化UI ======
        self.initUi()

    def initUi(self):
        self.setWindowTitle("AudioClipZ - 歌曲列表")
        self.resize(600, 400)

        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titleLabel.setStyleSheet("font-size: 22px; font-weight: bold;")

        self.numList.setFixedWidth(50)
        self.numList.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.numList.setStyleSheet("color: gray; font-weight: bold;")
        self.numList.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.numList.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.numList.setSelectionMode(QListWidget.SelectionMode.NoSelection)

        self.songList.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.songList.setSelectionMode(QListWidget.SelectionMode.SingleSelection)

        # 列表区
        listLayout = QHBoxLayout()
        listLayout.addWidget(self.numList)
        listLayout.addWidget(self.songList)

        # 主布局
        layout = QVBoxLayout(self)
        layout.addWidget(self.titleLabel)
        layout.addLayout(listLayout)

        # 按钮区
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.shuffleButton)
        buttonLayout.addWidget(self.editButton)
        buttonLayout.addStretch()
        layout.addLayout(buttonLayout)

        # 信号连接
        self.shuffleButton.clicked.connect(self.shuffleSongs)
        self.editButton.clicked.connect(self.enterClipEditor)
        self.songList.model().rowsMoved.connect(self.syncScroll)

        self.loadSongs()

    def loadSongs(self):
        audioExtensions = (".mp3", ".wav", ".flac", ".ogg", ".aac")
        for file in os.listdir(self.folderPath):
            if file.lower().endswith(audioExtensions):
                self.songNames.append(file)
                shutil.copy(os.path.join(os.path.abspath(self.folderPath), file), "Data/Temp")

        self.populateLists(self.songNames)

    def populateLists(self, names: list[str]):
        self.songList.clear()
        self.numList.clear()
        for i, name in enumerate(names, start=1):
            self.songList.addItem(QListWidgetItem(name))
            self.numList.addItem(QListWidgetItem(f"{i:02d}"))

    def shuffleSongs(self):
        shuffled = self.songNames[:]
        random.shuffle(shuffled)
        self.populateLists(shuffled)

    def syncScroll(self):
        pass  # 编号列表不变，无需同步

    def enterClipEditor(self):
        orderedSongs = [self.songList.item(i).text() for i in range(self.songList.count())]
        self.clipEditorWidget = ClipEditorWidget(orderedSongs)
        self.clipEditorWidget.show()
        self.close()


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    folder = r"D:\myProgramFiles\coding\projects\pycharmProjects\logiZ\Tests\testData"  # 替换为实际文件夹路径
    window = SongListWidget(folder)
    window.show()
    sys.exit(app.exec())