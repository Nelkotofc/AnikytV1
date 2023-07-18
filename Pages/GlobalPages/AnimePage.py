from __init__ import *

class AnimePage(QMainWindow):
    def __init__(self, manager):
        super(AnimePage, self).__init__()
        self.manager = manager
        self.listPage = ListPage(self, self.manager)
        # self.gridPage = GridPage(self.manager)
        self.widgets()

    def widgets(self):

        self.setCentralWidget(None)

        if self.manager.anilist.user is not None and self.manager.anilist.user.verified is True:
            if self.manager.option("DisplayModel") == "grid":
                self.gridLayout()
            elif self.manager.option("DisplayModel") == "list":
                self.listLayout()

        if self.centralWidget() is None:
            self.setCentralWidget(QWidget())


        self.manager.application(self)
        self.manager.defaultSwitchBar(self, self.centralWidget())

    def gridLayout(self):
        pass

    def listLayout(self):

        self.listPage.initUI(self.manager.anilist.user.aniMediaList.myanimemedias)
        self.setCentralWidget(self.listPage.widget)

