from pydub import AudioSegment
from os import path, remove
import tempfile

class Clip:
    __filePath = "Data/Temp"
    __tempFilesList = {}
    __songList = []
    __songListSet = set()

    def setFilePath(self, filePath):
        self.__filePath = filePath

    def applyEffects(self, fileName: str, volume: float, fadein: float, fadeout: float, startTime: int, endTime: int) -> int:
        seg = AudioSegment.from_file(path.join(path.abspath(self.__filePath), fileName))

        if startTime >= endTime:
            return 0

        seg = seg[startTime*1000 : endTime*1000]
        seg = seg.apply_gain(volume)
        if fadein != 0.0:
            seg = seg.fade_in(int(fadein*1000))
        if fadeout != 0.0:
            seg = seg.fade_out(int(fadeout*1000))

        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        seg.export(temp.name, format="mp3")
        self.__tempFilesList[fileName] = temp.name
        temp.close()

        return 1

    def combineClips(self, savedPath: str) -> int:
        combined = AudioSegment.empty()

        for fileName in self.__songList:
            seg = AudioSegment.from_file(self.__tempFilesList[fileName])
            combined += seg

        combined.export(savedPath, format="mp3")

        return 1

    def addTempFile(self, fileName: str):
        if fileName in self.__songListSet:
            return None

        self.__songListSet.add(fileName)
        self.__songList.append(fileName)

        seg = AudioSegment.from_file(path.join(path.abspath(self.__filePath), fileName))
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        seg.export(temp.name, format="mp3")
        self.__tempFilesList[fileName] = temp.name
        temp.close()
        return None

    def getTempFile(self, fileName: str):
        return self.__tempFilesList[fileName]

    def cleanTempFiles(self):
        for tempFile in self.__tempFilesList.values():
            try:
                remove(tempFile)
            except Exception as e:
                print(f"Error deleting temp file {tempFile}: {e}")