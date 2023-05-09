class QSSLoader:
    def __init__(self):
        pass

    @staticmethod
    def readFile(fileName):
        with open(fileName,'r',encoding='UTF-8') as file:
            return file.read()