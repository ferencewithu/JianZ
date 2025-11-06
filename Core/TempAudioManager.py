import atexit, tempfile, os

class TempAudioManager:
    __tempFilesList = []

    def create(self, suffix=".mp3"):
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        self.__tempFilesList.append(temp.name)
        temp.close()

    def cleanup(self):
        for path in self.__tempFilesList:
            os.remove(path)