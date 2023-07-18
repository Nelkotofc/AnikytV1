from __init__ import *

class AniGlob:
    def __init__(self, MediaType, per_page=10, start_page=None):
        if start_page is None:
            start_page = {}
        self.per_page = per_page
        self.MediaType = MediaType
        self.start_page = start_page
        self.topRanked = self.getTop("SCORE_DESC", start_page.get("Top Ranked"))
        self.topPopular = self.getTop("POPULARITY_DESC", start_page.get("Top Popular"))
        self.topTrend = self.getTop("TRENDING_DESC", start_page.get("Top Trending"))
        self.topFavourites = self.getTop("FAVOURITES_DESC", start_page.get("Top Favourites"))
        self.lastUpdated = self.getTop("UPDATED_AT_DESC", start_page.get("LastUpdated"))

        self.media_sorts = ['ID', 'ID_DESC',
                            'TITLE_ROMAJI', 'TITLE_ROMAJI_DESC', 'TITLE_ENGLISH', 'TITLE_ENGLISH_DESC', 'TITLE_NATIVE',
                            'TITLE_NATIVE_DESC',
                            'TYPE', 'TYPE_DESC',
                            'FORMAT', 'FORMAT_DESC',
                            'START_DATE', 'START_DATE_DESC',
                            'END_DATE', 'END_DATE_DESC',
                            'SCORE', 'SCORE_DESC',
                            'POPULARITY', 'POPULARITY_DESC',
                            'TRENDING', 'TRENDING_DESC',
                            'EPISODES', 'EPISODES_DESC',
                            'DURATION', 'DURATION_DESC',
                            'STATUS', 'STATUS_DESC',
                            'CHAPTERS', 'CHAPTERS_DESC',
                            'VOLUMES', 'VOLUMES_DESC',
                            'UPDATED_AT', 'UPDATED_AT_DESC',
                            'SEARCH_MATCH',
                            'FAVOURITES', 'FAVOURITES_DESC']

    def getTop(self, MediaSort, start_page=None):

        if start_page is None:
            start_page = 0

        query = """
            query ($page: Int!, $perPage: Int!, $sort: MediaSort, $type: MediaType) {
                Page (page: $page, perPage: $perPage) {
                    media (sort: [$sort], type: $type) {
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
                        chapters
                        volumes
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
            """

        var = {"page": 1, "perPage": self.per_page+start_page, "sort": MediaSort, "type": self.MediaType}

        response = requests.post('https://graphql.anilist.co', json={'query': query, 'variables': var})

        # Check if the request was successful
        if response.status_code == 200:
            # Extract the top anime data from the response
            result = []
            top_anime = response.json()["data"]["Page"]["media"]
            for x, animeJson in enumerate(top_anime):
                if x >= start_page:
                    result.append(AniMedia(self.MediaType, animeJson))

            return result
        else:
            print(f"Error: {response.status_code}")
            return None
