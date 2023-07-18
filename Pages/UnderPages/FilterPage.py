from __init__ import *
class FilterPage(QMainWindow):
    def __init__(self, manager):
        super(FilterPage, self).__init__()

        self.manager = manager

        self.centralArea = QWidget()
        self.setCentralWidget(self.centralArea)

        self.manager.application(self)