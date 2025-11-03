import sys, os, shutil
from PyQt6.QtWidgets import QApplication
from UI.MainWindow import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    if not app.exec():
        shutil.rmtree("Data/Temp")
        os.makedirs("Data/Temp", exist_ok=True)
        sys.exit()

if __name__ == "__main__":
    main()
