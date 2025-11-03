from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFileDialog
)
from PyQt6.QtCore import Qt
from UI.SongListWidget import SongListWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # ====== UI部件 ======
        self.titleLabel = QLabel("AudioClipZ")
        self.pathInput = QLineEdit()
        self.importButton = QPushButton("导入")


        # ====== 其他对象 ======
        self.songListWidget = None

        # ====== 初始化UI ======
        self.initUi()

    def initUi(self):
        self.setWindowTitle("AudioClipZ - 首页")
        self.setFixedSize(400, 300)

        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titleLabel.setStyleSheet("font-size: 28px; font-weight: bold;")
        self.pathInput.setPlaceholderText("导入文件地址")

        inputLayout = QHBoxLayout()
        inputLayout.addWidget(self.pathInput)
        inputLayout.addWidget(self.importButton)

        layout = QVBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.titleLabel, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(inputLayout)
        layout.addStretch(1)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        self.importButton.clicked.connect(self.openImport)

    def openImport(self):
        folder = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder:
            self.pathInput.setText(folder)
            self.songListWidget = SongListWidget(folder)
            self.songListWidget.show()
            self.close()