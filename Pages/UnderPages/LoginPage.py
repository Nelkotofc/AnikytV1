from __init__ import *
class LoginPage(QMainWindow):
    def __init__(self, manager):
        super(LoginPage, self).__init__()

        self.manager = manager
        self.manager.anilist.accessToken = self.getToken

        self.widgets()

    def widgets(self):

        self.centralArea = QWidget()
        self.setCentralWidget(self.centralArea)

        self.button = QPushButton("<--", self.centralArea)
        self.button.setStyleSheet(
            f"font-size: 20px; font-weight: bold; background: transparent; border: {'black' if self.manager.option('DisplayColor') == 'white' else 'white'}")
        self.button.setGeometry(0, 0, 40, 30)
        self.button.clicked.connect(self.manager.previousPage)

        self.userNameInput = QLineEdit(self.centralArea)
        self.userNameInput.setStyleSheet("font-size: 20px;")
        self.userNameInput.setAlignment(Qt.AlignCenter)
        self.userNameInput.setGeometry(40, 0, self.width() * 2 - 100, 50)

        self.addAccountButton = QPushButton("ADD", self.centralArea)
        self.addAccountButton.setGeometry(self.userNameInput.width() + self.userNameInput.x(), 0, 60, 50)
        self.addAccountButton.clicked.connect(self.addAccount)

        self.position = [0, 50]

        self.setAccounts()

        self.manager.application(self)


    def setGeometry(self, sender, width, height):
        if sender != self.manager.anilist.user:
            sender.setGeometry(self.position[0], self.position[1], 200, 200)
            self.position[0] += 200
            if self.position[0] > self.width() - 200:
                self.position[1] += 200
                self.position[0] = 0

    def setAccounts(self): # Displays previous accounts

        for x, accountName in enumerate(list(self.manager.anilist.aniAccounts.keys())):
            account: AniAccount = self.manager.anilist.aniAccounts[accountName]
            userName = self.manager.anilist.user.username if self.manager.anilist.user is not None else None

            if accountName != userName:
                qib = QImageButton(account, account.information["avatar"]["large"], size=(None, 100),
                                   loaded=self.setGeometry, args=[accountName, self.centralArea])
                qib.clicked.connect(self.preAccount)
                qib.setStyleSheet("font-size: 20px; font-weight: bold;")

    def loadAccount(self, account): # Send datas (saves, page switch, widgets, login)
        print(account.username)
        self.manager.anilist.login(account)
        self.manager.anilist.save_account()
        self.manager.anilist.save_user()

        self.manager.animePage.reload()
        self.manager.mangaPage.reload()

        self.manager.animePageSwitch()
        self.widgets()
    def preAccount(self): # Click on account button
        sender: QImageButton = self.sender()
        self.loadAccount(sender.aniMedia)

    def getToken(self, tokenPage):
        pass

    def addAccount(self): # Add a new account
        load = False
        if self.userNameInput.text() not in self.manager.anilist.aniAccounts:
            aniAccount = AniAccount(self.userNameInput.text())
            aniAccount.verify_account(self.manager.anilist)
            if aniAccount.verified:
                load = True

        else:
            aniAccount = self.manager.anilist.aniAccounts[self.userNameInput.text()]
            load = True

        if load:
            self.loadAccount(aniAccount)
