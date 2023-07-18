from __init__ import *


class Settings:
    def __init__(self, manager, **kwargs):
        self.options = kwargs
        self.manager = manager

    def setOption(self, key, value):
        self.options[key] = value
        self.reload()

    def reload(self):
        self.manager.styleCreate()

    def homePageSwitch(self):
        self.manager.switchPage("HomePage", self.manager.homePage)

    def animePageSwitch(self):
        self.manager.switchPage("AnimePage", self.manager.animePage)

    def settingsPageSwitch(self):
        self.manager.switchPage("SettingsPage", self.manager.settingsPage)

    def mangaPageSwitch(self):
        self.manager.switchPage("MangaPage", self.manager.mangaPage)

    def profilePageSwitch(self):
        self.manager.switchPage("ProfilePage", self.manager.profilePage)

    def mediaPageSwitch(self, aniMedia):
        self.manager.mediaPage.loadPage(aniMedia)
        self.manager.switchPage("MediaPage", self.manager.mediaPage)

    def loginPageSwitch(self):
        self.manager.switchPage("LoginPage", self.manager.loginPage)

    def defaultSwitchBar(self, window: QMainWindow, area):

        settingsPage_button = QPushButton("Settings", area)
        settingsPage_button.clicked.connect(self.settingsPageSwitch)

        homePage_button = QPushButton("Home", area)
        homePage_button.clicked.connect(self.homePageSwitch)

        animePage_button = QPushButton("Anime", area)
        animePage_button.clicked.connect(self.animePageSwitch)

        mangaPage_button = QPushButton("Manga", area)
        mangaPage_button.clicked.connect(self.mangaPageSwitch)

        profilePage_button = QPushButton("Profile", area)
        profilePage_button.clicked.connect(self.profilePageSwitch)

        width, height = window.width() / 5, 30

        self.buttonLists(window, 0, window.height() - height, width, height,
                         [profilePage_button, mangaPage_button, homePage_button,
                          animePage_button, settingsPage_button])

    @staticmethod
    def buttonLists(window: QMainWindow, x, y, width, height, buttons, margin_x=0, margin_y=0):

        start_x = copy.copy(x)

        for btn in buttons:
            btn: QPushButton
            btn.setGeometry(x, y, width, height)
            x += width + margin_x
            if x >= window.width():
                y += height + margin_y
                x = copy.copy(start_x)

        return x, y

    def application(self, window: QMainWindow):
        window.setWindowTitle(self.option("WindowTitle"))
        window.setWindowIcon(QIcon(self.option("WindowIcon")))
        window.setFixedSize(*self.option("WindowSize"))

    def option(self, key, otherwise=None):
        value = self.options.get(key)

        if value is None:
            return otherwise

        return value


class Manager(Settings):
    def __init__(self, **kwargs):
        super(Manager, self).__init__(self, **kwargs)

        self.begin = None

        self.app = QApplication()

        self.anilist = Anilist(self.option("accID"), None, self.option("acctJson"), self.option("userJson"))
        self.anilist.load_accounts()
        self.anilist.load_user()

        if self.anilist.user is not None:
            self.anilist.login(self.anilist.user)

        self.styleCreate()

        self.Pages = []
        self.BeenPages = {}
        self.currentPage = None

        self.filterPage = FilterPage(self)
        self.friendPage = FriendPage(self)
        self.loginPage = LoginPage(self)
        self.mediaPage = MediaPage(self)

        self.homePage = HomePage(self)
        self.animePage = AnimePage(self)
        self.mangaPage = MangaPage(self)
        self.profilePage = ProfilePage(self)
        self.settingsPage = SettingsPage(self)

        self.switchPage("HomePage", self.homePage)
        self.app.exec()

    def styleCreate(self):
        stylesheet = f"""
                QWidget {{
                  background-color: {self.option("DisplayColor")};
                }}
                QMainWindow {{
                  background-color: {self.option("DisplayColor")};
                }}
                QLabel {{
                  color: {"black" if self.option("DisplayColor") == "white" else "white"};
                }}
                QLineEdit {{
                  background-color: {self.option("DisplayColor")};
                  color: {"black" if self.option("DisplayColor") == "white" else "white"};
                }}
                QCheckBox {{
                  color: {"black" if self.option("DisplayColor") == "white" else "white"}
                }}
                QPushButton {{
                  background-color: {self.option("DisplayColor")};
                  color: {"black" if self.option("DisplayColor") == "white" else "white"};
                  border: 1px solid {"black" if self.option("DisplayColor") == "white" else "white"};
                }}
                QListWidget {{
                  background-color: {self.option("DisplayColor")};
                  color: {"black" if self.option("DisplayColor") == "white" else "white"};
                }}
                """

        self.app.setStyleSheet(stylesheet)

    def previousPage(self):
        print(f"Backing up")

        page = self.Pages[-1]
        self.Pages.pop(-1)

        page.move(self.currentPage.pos())
        self.currentPage.hide()
        self.Pages.append(self.currentPage)

        self.currentPage = page
        self.currentPage.show()

    def switchPage(self, tag, page):
        print(f"Switching to {page}")

        if self.currentPage is not None:
            page.move(self.currentPage.pos())
            self.currentPage.hide()
            self.Pages.append(self.currentPage)

        self.currentPage = page
        self.currentPage.show()

        if tag not in self.BeenPages:
            self.BeenPages[tag] = 0

        self.BeenPages[tag] += 1

        if tag == 'AnimePage' and self.BeenPages[tag] == 1:
            self.animePage.widgets()

        if tag == 'MangaPage' and self.BeenPages[tag] == 1:
            self.mangaPage.widgets()




