from __init__ import *


class AniMediaList:
    def __init__(self, account):
        self.myanimemedias = self.register(account, "ANIME")
        self.mymangamedias = self.register(account, "MANGA")

    def getMyAniMedia(self, aniMedia):
        animeAnswers = [myaniMedia for myaniMedia in self.myanimemedias if myaniMedia.id == aniMedia.id]
        if len(animeAnswers) > 0:
            return animeAnswers[0]
        mangaAnswers = [myaniMedia for myaniMedia in self.mymangamedias if myaniMedia.id == aniMedia.id]
        if len(mangaAnswers) > 0:
            return mangaAnswers[0]
        return None

    def register(self, account, type):
        mymedias = []
        query = '''
                            query ($userName: String!, $type: MediaType) {
                              MediaListCollection (userName: $userName, type: $type) {
                                lists {
                                  name
                                  entries {
                                    progress
                                    score
                                    status
                                    media {
                                      id
                                      status
                                      format
                                      description
                                      endDate {
                                        year
                                        month
                                        day
                                      }
                                      season
                                      seasonYear
                                      seasonInt
                                      duration
                                      countryOfOrigin
                                      volumes
                                      chapters
                                      trailer {
                                        site
                                        thumbnail
                                      }
                                      coverImage {
                                        extraLarge
                                        large
                                        medium
                                      }
                                      bannerImage
                                      synonyms
                                      meanScore
                                      popularity
                                      trending
                                      favourites
                                      isFavourite
                                      averageScore
                                      episodes
                                      isAdult
                                      nextAiringEpisode {
                                        episode
                                        timeUntilAiring
                                      }
                                      genres
                                      startDate {
                                        year
                                        month
                                        day
                                      }
                                      title {
                                        english
                                        romaji
                                        native
                                      }
                                      relations {
                                        edges {
                                          relationType
                                          node {
                                            id
                                          }
                                        }
                                      }
                                    }
                                  }
                                }
                              }
                            }
                            '''

        variables = {'userName': account.username, 'type': type}

        anilist_response = requests.post('https://graphql.anilist.co', json={'query': query, 'variables': variables})

        if anilist_response.status_code != 200:
            quit(f"Error getting media list: {anilist_response.json()}")
        else:

            for category_json in anilist_response.json()['data']['MediaListCollection']['lists']:
                category_name = category_json['name']
                category_entries = category_json['entries']
                for media_json in category_entries:
                    mymedias.append(MyAniMedia("ANIME", media_json, category_name))
            return mymedias