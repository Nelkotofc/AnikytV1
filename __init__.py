import requests
import copy
import json
from datetime import date

from Adds.QImageButton import QImageButton

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from Anilist.AniMedias import MyAniMedia
from Anilist.AniMediaList import AniMediaList
from Anilist.AniAccount import AniAccount
from Anilist.Anilist import Anilist

from Anilist.AniMedias import AniMedia
from Anilist.AniGlob import AniGlob

from Pages.UnderPages.MediaPage import MediaPage
from Pages.UnderPages.LoginPage import LoginPage
from Pages.UnderPages.FriendPage import FriendPage
from Pages.UnderPages.FilterPage import FilterPage
from Pages.UnderPages.ListPage import ListPage

from Pages.GlobalPages.ProfilePage import ProfilePage
from Pages.GlobalPages.MangaPage import MangaPage
from Pages.GlobalPages.AnimePage import AnimePage
from Pages.GlobalPages.SettingsPage import SettingsPage
from Pages.GlobalPages.HomePage import HomePage

from application import Manager







