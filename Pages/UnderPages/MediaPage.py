from __init__ import *


class MediaPage(QMainWindow):
    def __init__(self, manager):
        super(MediaPage, self).__init__()

        self.centralArea = None
        self.manager = manager

    def menuBarUpdate(self, width, Labels):
        self.preStyleSheet(Labels)
        for x, label in enumerate(Labels):
            label.setGeometry(width + (self.width() - width) / len(Labels) * x, 30,
                              (self.width() - width) / len(Labels), 20)
            label.setAlignment(Qt.AlignCenter)

    def GeometryImage(self, sender, width, height):
        self.CoverImage.setGeometry(0, 0, width, height)
        aniMedia = self.CoverImage.aniMedia

        self.TitleLabel.setGeometry(width, 0, self.width() - width, 30)
        self.TitleLabel.setAlignment(Qt.AlignCenter)

        self.DescriptionLabel.setGeometry(width, 50, self.width() - width, 500)
        self.DescriptionLabel.setAlignment(Qt.AlignCenter)
        self.DescriptionLabel.setWordWrap(True)
        self.DescriptionLabel.adjustSize()
        self.DescriptionLabel.setGeometry(width, 50, self.width() - width, self.DescriptionLabel.height())

        self.DateLabel.setGeometry(width, 50 + self.DescriptionLabel.height(), self.width() - width, 40)
        self.DateLabel.setAlignment(Qt.AlignCenter)

        globLists = [self.FormatLabel, self.StatusLabel]

        if aniMedia.mediaType == "MANGA" or aniMedia.format == "MANGA":

            globLists += [self.ChaptersLabel, self.VolumesLabel]
        elif aniMedia.mediaType == "ANIME":

            globLists += [self.SeasonLabel, self.SeasonYearLabel, self.AiredEpisodesLabel, self.TotalEpisodesLabel,
                          self.DurationLabel]

        globLists += [self.MeanScoreLabel, self.CountryLabel, self.isAdultLabel]

        while None in globLists:
            globLists.remove(None)

        self.menuBarUpdate(width, globLists)

        # Add Labels and buttons


    def preStyleSheet(self, Labels):
        for Label in Labels:
            Label.setStyleSheet(
                f"border: 2px solid {'black' if self.manager.option('DisplayColor') == 'white' else 'white'};")

    def previousButton(self):
        button = QPushButton("<--", self.centralArea)
        button.setStyleSheet(
            f"font-size: 20px; font-weight: bold; background: transparent; border: {'black' if self.manager.option('DisplayColor') == 'white' else 'white'}")
        button.setGeometry(0, 0, 40, 30)
        button.clicked.connect(self.manager.previousPage)

    def mangaPage(self, aniMedia):

        self.ChaptersLabel = QLabel(str(aniMedia.chapters) + " chap", self.centralArea)
        self.VolumesLabel = QLabel(str(aniMedia.volumes) + " vol", self.centralArea)

    def animePage(self, aniMedia):
        self.SeasonLabel = QLabel(str(aniMedia.season), self.centralArea)

        airedEpisodes = aniMedia.getAiredEpisodes()

        self.AiredEpisodesLabel = None
        if airedEpisodes != aniMedia.episodes:
            self.AiredEpisodesLabel = QLabel(str(airedEpisodes).upper() + " Aep", self.centralArea)

        self.TotalEpisodesLabel = None

        if aniMedia.episodes is not None:
            self.TotalEpisodesLabel = QLabel(str(aniMedia.episodes).upper() + " ep", self.centralArea)

        self.SeasonYearLabel = QLabel(str(aniMedia.seasonYear), self.centralArea)
        self.DurationLabel = QLabel(str(aniMedia.duration) + " min", self.centralArea)

    def loadPage(self, aniMedia):

        self.centralArea = QWidget()
        self.setCentralWidget(self.centralArea)
        if aniMedia.mediaType == "MANGA" or aniMedia.format == "MANGA":
            self.mangaPage(aniMedia)
        elif aniMedia.mediaType == "ANIME":
            self.animePage(aniMedia)

        self.TitleLabel = QLabel(aniMedia.getTitle(romaji=self.manager.option("romaji")), self.centralArea)
        self.TitleLabel.setStyleSheet(f"font-size: 20px; font-weight: bold;")

        self.DescriptionLabel = QLabel(aniMedia.description, self.centralArea)
        self.DescriptionLabel.setStyleSheet(
            f"border: 1px solid {'black' if self.manager.option('DisplayColor') == 'white' else 'white'};")

        self.StatusLabel = QLabel(aniMedia.status, self.centralArea)
        self.FormatLabel = QLabel(aniMedia.format, self.centralArea)
        self.CountryLabel = QLabel(aniMedia.countryOfOrigin.upper(), self.centralArea)
        self.MeanScoreLabel = QLabel(str(aniMedia.meanScore) + "%", self.centralArea)
        self.isAdultLabel = QLabel("Adult : " + str(aniMedia.isAdult).upper(), self.centralArea)

        startDate = str(aniMedia.startDate.strftime("%B %d, %Y")) if aniMedia.startDate is not None else "_____"
        endDate = str(aniMedia.endDate.strftime("%B %d, %Y")) if aniMedia.endDate is not None else "_____"

        self.DateLabel = QLabel(startDate + " - " + endDate, self.centralArea)

        self.CoverImage = QImageButton(aniMedia, aniMedia.coverImage["extraLarge"], args=[self.centralArea],
                                       loaded=self.GeometryImage)

        self.previousButton()
        self.manager.application(self)  # self.manager.defaultSwitchBar(self, self.centralArea)
