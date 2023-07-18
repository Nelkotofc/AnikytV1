from __init__ import *


def reDate(DateJson):
    try:
        return date(DateJson["year"], DateJson["month"], DateJson["day"])
    except:
        return None


class AniMedia:
    def __init__(self, mediaType, json):
        self.id = json["id"]
        self.status = json["status"]  #
        self.mediaType = mediaType
        self.format = json["format"]  #
        self.description = json["description"]  #
        self.endDate = reDate(json["endDate"])
        self.season = json["season"]  #
        self.seasonYear = json["seasonYear"]  #
        self.seasonInt = json["seasonInt"]
        self.duration = json["duration"]  #
        self.countryOfOrigin = json["countryOfOrigin"]
        self.trailer = json["trailer"]
        self.coverImage = json["coverImage"]  #
        self.bannerImage = json["bannerImage"]
        self.synonyms = json["synonyms"]
        self.meanScore = json["meanScore"]
        self.popularity = json["popularity"]
        self.trending = json["trending"]
        self.favourites = json["favourites"]
        self.isFavourite = json["isFavourite"]
        self.averageScore = json["averageScore"]
        self.episodes = json["episodes"]  #
        self.isAdult = json["isAdult"]
        self.nextAiringEpisode = json["nextAiringEpisode"]  #
        self.genres = json["genres"]
        self.startDate = reDate(json["startDate"])
        self.title = json["title"]  #
        self.relations = json["relations"]
        self.chapters = json["chapters"]
        self.volumes = json["volumes"]

    def nextAiringTime(self):
        try:
            seconds: int = self.nextAiringEpisode["timeUntilAiring"]

            years = int(seconds / (365.25 * 24 * 60 * 60))
            seconds -= years * 365.25 * 24 * 60 * 60

            months = int(seconds / (30 * 24 * 60 * 60))
            seconds -= months * 30 * 24 * 60 * 60

            weeks = int(seconds / (7 * 24 * 60 * 60))
            seconds -= weeks * 7 * 24 * 60 * 60

            days = int(seconds / (24 * 60 * 60))
            seconds -= days * 24 * 60 * 60

            hours = int(seconds / (60 * 60))
            seconds -= hours * 60 * 60

            minutes = int(seconds / 60)
            seconds -= minutes * 60

            return years, months, weeks, days, hours, minutes, seconds
        except:
            return None

    def nextAiringTimeText(self):

        nextAT = self.nextAiringTime()
        if nextAT is None:
            return None

        years, months, weeks, days, hours, minutes, seconds = nextAT

        timeText = ""

        def add(text, value, name):
            if value > 0:
                text += f"{value} {name} "
            return text
        timeText = add(timeText, years, "years")
        timeText = add(timeText, months, "months")
        timeText = add(timeText, weeks, "weeks")
        timeText = add(timeText, days, "days")
        timeText = add(timeText, hours, "hours")
        timeText = add(timeText, minutes, "minutes")
        timeText = add(timeText, seconds, "seconds")

        return timeText[:-1]

    def getAiredEpisodes(self):
        try:

            if (date.today() - self.startDate).total_seconds() >= 0:

                if self.nextAiringEpisode is None:
                    media_aired_episodes = self.episodes
                else:
                    media_aired_episodes = self.nextAiringEpisode["episode"] - 1
                return media_aired_episodes
            else:
                return 0
        except:
            pass
        return None

    def getTitle(self, romaji):
        if not romaji and self.title["english"] is not None:
            return self.title["english"]
        return self.title["romaji"]


class MyAniMedia(AniMedia):
    def __init__(self, mediaType, json, category):
        super().__init__(mediaType, json["media"])
        self.category = category
        self.progress = json["progress"]
        self.score = json["score"]
        self.mystatus = json["status"]
