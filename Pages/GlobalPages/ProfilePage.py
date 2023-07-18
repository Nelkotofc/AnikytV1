from __init__ import *


class ProfilePage(QMainWindow):
    def __init__(self, manager):
        super(ProfilePage, self).__init__()

        self.manager = manager

        self.centralArea = QWidget()
        self.setCentralWidget(self.centralArea)

        self.manager.application(self)
        self.manager.defaultSwitchBar(self, self.centralArea)