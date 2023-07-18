from PySide6.QtCore import QSize, QUrl
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PySide6.QtWidgets import QPushButton


class QImageButton(QPushButton):
    def __init__(self, aniMedia, url, size=None, divider=None, loaded=None, args=None):
        if args is None:
            args = []
        super().__init__(*args)

        self.aniMedia = aniMedia
        self.SizeVar = size
        self.DividerVar = divider
        self.pixmap = None
        self.loaded = loaded

        self.network_manager = QNetworkAccessManager()
        self.network_manager.finished.connect(self.on_image_download_finished)

        request = QNetworkRequest(QUrl(url))
        self.network_manager.get(request)

    def on_image_download_finished(self, reply):
        if str(reply.error()) == "NetworkError.NoError":

            data = reply.readAll()

            self.pixmap = QPixmap()
            self.pixmap.loadFromData(data)

            if self.SizeVar is not None:

                if self.SizeVar[1] is not None:
                    self.pixmap = self.pixmap.scaledToHeight(self.SizeVar[1])
                elif self.SizeVar[0] is not None:
                    self.pixmap = self.pixmap.scaledToWidth(self.SizeVar[0])

                Size = QSize(self.pixmap.width(), self.pixmap.height())

                self.setIconSize(Size)
                self.setGeometry(self.x(), self.y(), Size.width(), Size.height())
            else:
                self.DividerVar = self.DividerVar if self.DividerVar is not None else 1

                Size = QSize(self.pixmap.width() / self.DividerVar, self.pixmap.height() / self.DividerVar)

            self.setIconSize(Size)  # Set the desired icon size
            self.setGeometry(self.x(), self.y(), Size.width(), Size.height())

            # Set the pixmap as the icon for the button
            self.setIcon(QIcon(self.pixmap))  #
            if self.loaded is not None:
                self.loaded(self, self.pixmap.width(), self.pixmap.height())
        else:
            print("Error downloading image:", reply.errorString())
