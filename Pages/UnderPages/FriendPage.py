from __init__ import *
class FriendPage(QMainWindow):
    def __init__(self, manager):
        super(FriendPage, self).__init__()

        self.manager = manager

        self.centralArea = QWidget()
        self.setCentralWidget(self.centralArea)

        self.manager.application(self)