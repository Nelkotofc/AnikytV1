from __init__ import *


class HomePage(QMainWindow):
    def __init__(self, manager):
        super(HomePage, self).__init__()

        self.manager = manager
        self.animeGlob = AniGlob("ANIME", 10)  # 1-11 (8+)
        self.mangaGlob = AniGlob("MANGA", 10)  # 1-11 (8+)

        self.topNext = {}
        self.centralArea = None
        self.layout = None
        self.itemOn = None
        self.animeLayout()

    def onMediaClicked(self):
        aniMedia: AniMedia = self.sender().aniMedia
        self.manager.mediaPageSwitch(aniMedia)

    def FinishLayout(self, grid):

        self.layout.addLayout(grid, 0, 1)
        self.centralArea.setLayout(self.layout)
        self.manager.application(self)
        self.manager.defaultSwitchBar(self, self.centralArea)

    def loadLayout(self):
        self.centralArea = QWidget()
        self.setCentralWidget(self.centralArea)
        self.layout = None
        self.centralArea.setLayout(self.layout)
        self.MediaTypeList = QListWidget()
        self.MediaTypeList.addItems(["Anime", "Manga"])
        self.MediaTypeList.itemClicked.connect(self.onListItemClicked)

        self.layout = QGridLayout()
        self.layout.addWidget(self.MediaTypeList, 0, 0)

    def DefaultLayout(self, GlobLists):
        self.loadLayout()

        grid = QGridLayout()
        row = 1
        column = 1
        for listType in list(GlobLists.keys()):

            grid.addWidget(QLabel(f"<b>{listType}</b>"), row - 1, column)

            for aniMedia in GlobLists.get(listType):
                aniImgBtn = QImageButton(aniMedia, aniMedia.coverImage["extraLarge"], divider=4)
                aniImgBtn.clicked.connect(self.onMediaClicked)
                grid.addWidget(aniImgBtn, row, column)
                column += 1

            backarrow = QPushButton("<-")
            backarrow.clicked.connect(self.backPage)
            grid.addWidget(backarrow, row, column)
            self.topNext[backarrow] = listType

            column += 1

            nextarrow = QPushButton("->")
            nextarrow.clicked.connect(self.nextPage)
            self.topNext[nextarrow] = listType
            grid.addWidget(nextarrow, row, column)

            column = 1
            row += 2

        grid.addWidget(QLabel(), row - 1, column)
        self.FinishLayout(grid)

    def nextPage(self):
        if self.itemOn == "Anime":
            mT = self.animeGlob.MediaType
            pp = self.animeGlob.per_page
            sp = copy.copy(self.animeGlob.start_page)
            if self.topNext[self.sender()] in sp:
                sp[self.topNext[self.sender()]] += pp
            else:
                sp[self.topNext[self.sender()]] = pp

            self.animeGlob = AniGlob(mT, pp, sp)
            self.animeLayout()
        elif self.itemOn == "Manga":
            mT = self.mangaGlob.MediaType
            pp = self.mangaGlob.per_page
            sp = copy.copy(self.mangaGlob.start_page)
            if self.topNext[self.sender()] in sp:
                sp[self.topNext[self.sender()]] += pp
            else:
                sp[self.topNext[self.sender()]] = pp

            self.mangaGlob = AniGlob(mT, pp, sp)
            self.mangaLayout()

    def backPage(self):
        if self.itemOn == "Anime":
            mT = self.animeGlob.MediaType
            pp = self.animeGlob.per_page
            sp = copy.copy(self.animeGlob.start_page)
            if self.topNext[self.sender()] in sp and sp[self.topNext[self.sender()]] - pp >= 0:
                sp[self.topNext[self.sender()]] -= pp
                self.animeGlob = AniGlob(mT, pp, sp)
                self.animeLayout()
            else:
                sp[self.topNext[self.sender()]] = 0


        elif self.itemOn == "Manga":
            mT = self.mangaGlob.MediaType
            pp = self.mangaGlob.per_page
            sp = copy.copy(self.mangaGlob.start_page)
            if self.topNext[self.sender()] in sp and sp[self.topNext[self.sender()]] - pp >= 0:
                sp[self.topNext[self.sender()]] -= pp
                self.mangaGlob = AniGlob(mT, pp, sp)
                self.mangaLayout()
            else:
                sp[self.topNext[self.sender()]] = 0

    def animeLayout(self):

        self.itemOn = "Anime"

        GlobLists = {"Top Ranked": self.animeGlob.topRanked, "Top Popular": self.animeGlob.topPopular,
            "Top Trending": self.animeGlob.topTrend, "Top Favourites": self.animeGlob.topFavourites}

        self.DefaultLayout(GlobLists)

    def mangaLayout(self):

        self.itemOn = "Manga"

        GlobLists = {"Top Ranked": self.mangaGlob.topRanked, "Top Popular": self.mangaGlob.topPopular,
            "Top Trending": self.mangaGlob.topTrend, "Top Favourites": self.mangaGlob.topFavourites}

        self.DefaultLayout(GlobLists)

    def onListItemClicked(self, item):
        if item.text() == "Anime":
            self.animeLayout()
        elif item.text() == "Manga":
            self.mangaLayout()
