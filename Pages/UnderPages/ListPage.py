from __init__ import *


class ListPage:
    def __init__(self, mainWindow, manager):
        self.widget = QWidget()
        self.mainWindow = mainWindow
        self.manager = manager
        self.categoryBlock = []

    def onload_image(self, QIB, image_width, image_height):
        QIB.setFixedSize(QSize(image_width, image_height))

    def categoryBlocked(self, category):

        if category in self.categoryBlock:

            self.categoryBlock.remove(category)
        else:

            self.categoryBlock.append(category)
        self.mainWindow.widgets()

    def animePressedCall(self, aniMedia):
        def animePressed():
            self.manager.mediaPageSwitch(aniMedia)

        return animePressed

    def create(self, media, layout):
        # Same code as before...
        row_layout = QHBoxLayout()
        image_button = QImageButton(media, media.coverImage["large"],
                                    size=(None, 600 if self.manager.option("ModelSize") == "large" else 200),
                                    loaded=self.onload_image)  #
        image_button.clicked.connect(self.animePressedCall(media))
        name_label = QLabel(media.getTitle(self.manager.option("romaji")))
        row_layout.addWidget(image_button)
        row_layout.addWidget(name_label)
        layout.addLayout(row_layout)

        # Create the second row with additional buttons and information
        row_layout = QHBoxLayout()
        # button1 = QPushButton("Button 1")
        #  button2 = QPushButton("Button 2")
        information_label = QLabel(media.nextAiringTimeText())
        # row_layout.addWidget(button1)
        # row_layout.addWidget(button2)
        row_layout.addWidget(information_label)
        layout.addLayout(row_layout)

    def verifyMedia(self, myAniMedia: MyAniMedia):
        if self.manager.option("AdultMedias") is False:
            if myAniMedia.isAdult is True:
                return False

        return True

    def initUI(self, medias=None):

        self.widget = QWidget()

        self.widget.setLayout(None)

        medias: list[AniMedia]

        if medias is None:
            quit("There are no medias")

        main_layout = QHBoxLayout()

        # Create the layout for the buttons and information
        buttons_layout = QVBoxLayout()

        if self.manager.option("AllModel") is True:

            for media in list(medias):  # 5 is the number of animes
                if self.verifyMedia(media):
                    self.create(media, buttons_layout)
        else:
            lists = {}
            for media in list(medias):

                if self.verifyMedia(media):

                    cat = media.category if self.manager.option("CustomModel") is True else media.mystatus

                    if cat not in lists:
                        lists[cat] = []

                    lists[cat].append(media)

            for category in list(lists.keys()):

                row_layout = QHBoxLayout()

                category_btn = QPushButton(category)
                category_btn.setStyleSheet("font-weight: bold;")
                category_btn.clicked.connect(self.make_blockcall(category))

                row_layout.addWidget(category_btn)
                buttons_layout.addLayout(row_layout)

                if category not in self.categoryBlock:

                    for media in lists.get(category):
                        self.create(media, buttons_layout)

        row_layout = QHBoxLayout()
        row_layout.addWidget(QLabel())
        buttons_layout.addLayout(row_layout)

        # Create the scroll area to enable vertical scrolling
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Create a container widget for the anime information
        anime_container = QWidget()
        anime_container_layout = QVBoxLayout()
        anime_container_layout.addLayout(buttons_layout)
        anime_container.setLayout(anime_container_layout)
        scroll_area.setWidget(anime_container)

        main_layout.addWidget(scroll_area)

        self.widget.setLayout(main_layout)

    def make_blockcall(self, name):
        def blockcall():
            self.categoryBlocked(name)

        return blockcall

    def onSliderValueChanged(self, value):
        # Show the corresponding row based on the slider value
        buttons_layout = self.widget.layout().itemAt(0).widget().layout()
        for index in range(buttons_layout.count()):
            buttons_layout.itemAt(index).layout().setEnabled(index == value)
