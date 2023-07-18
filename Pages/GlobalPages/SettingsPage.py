from __init__ import *


class SettingsPage(QMainWindow):
    def __init__(self, manager):
        super(SettingsPage, self).__init__()

        self.manager = manager

        self.centralArea = QWidget()
        self.setCentralWidget(self.centralArea)

        reloadanimes = [self.manager.animePage.widgets, self.manager.mangaPage.widgets]

        self.options = {  # Checked Var, Unchecked Var, VarName, [Fonc, ...], Reversed
            'Dark Mode': ["black", "white", 'DisplayColor'],
            'Grid Display': ["grid", "list", "DisplayModel"],
            'Adult Medias': [True, False, None, reloadanimes],
            'English Titles': [False, True, "romaji", reloadanimes],
            'Large Icons': ["large", 'small', 'ModelSize', reloadanimes],
            'All Lists Together': [True, False, "AllModel", reloadanimes],
            'Custom Lists': [True, False, "CustomModel", reloadanimes]
        }

        self.loadSettings()

        self.manager.application(self)
        self.manager.defaultSwitchBar(self, self.centralArea)

    def getOptionName(self, option):
        return option.replace(" ", "") if self.options.get(option)[2] is None else self.options.get(option)[2]

    def nextValue(self, option):

        if self.manager.option(self.getOptionName(option)) == self.options.get(option)[0]:
            value = self.options.get(option)[1]
        else:
            value = self.options.get(option)[0]

        return value

    def checkEvent(self):
        textOption = self.sender().text()
        optName = self.getOptionName(textOption)
        value = self.nextValue(textOption)
        self.manager.setOption(optName, value)

        if len(self.options.get(textOption)) > 3 and self.options.get(textOption)[3] is not None:
            for fonc in self.options.get(textOption)[3]:
                try:
                    fonc(textOption, value)
                except:
                    try:
                        fonc()
                    except:
                        pass


    def getCheckBool(self, option):
        return True if self.manager.option(self.getOptionName(option)) == self.options.get(option)[
            0] else False

    def loadSettings(self):

        y = 0
        for option in self.options:
            checkBox = QCheckBox(option, self.centralArea)
            checkBox.setStyleSheet("font-size: 20px;")
            checkBox.setChecked(self.getCheckBool(option))
            checkBox.stateChanged.connect(self.checkEvent)
            checkBox.setGeometry(10, y, self.width(), 100)
            y += checkBox.height()

        loginBtn = QPushButton("Login", self.centralArea)
        loginBtn.setStyleSheet("font-size: 20px; font-weight: bold;")
        width = 300
        height = 50
        loginBtn.setGeometry(self.width() - width / 2, self.height() - height / 2, width, height)
        loginBtn.clicked.connect(self.manager.loginPageSwitch)

