from __init__ import *


class AniAccount:

    def __init__(self, username):
        self.username = username
        self.verified = 0
        self.token = None
        self.information = None
        self.aniMediaList = None

    def AdaptUser(self, query, variables):
        # Define the request headers
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        # Send the API request
        response = requests.post("https://graphql.anilist.co", headers=headers,
                                 json={"query": query, "variables": variables})

        # Process the response
        if response.status_code == 200:
            data = response.json()
            if "errors" in data:
                quit(f"Error: {data['errors']}")
                return False
            else:
                return True
        else:
            quit(f"Request failed: {response.status_code}")

    def getUser(self):

        query = '''
                query ($userName: String!) {
                  User (name: $userName) {
                    id
                    name
                    avatar {
                      large
                      medium
                    }
                  }
                }
                '''

        var = {
            "userName": self.username
        }

        anilist_response = requests.post('https://graphql.anilist.co',
                                         json={'query': query, 'variables': var})

        if anilist_response.status_code != 200:
            self.information = None
        else:
            AniJson = anilist_response.json()

            self.information = AniJson["data"]["User"]

    def verify_account(self, AniL):
        self.getUser()

        if self.information is not None:
            token = AniL.accessToken(AniL.getTokenPage())

            # Testing Token !!

            self.token = token

            AniL.accounts[self.username] = [self.information, self.token]
            self.verified = True
        else:
            self.verified = False
        return self.verified

    def login(self):
        self.aniMediaList = AniMediaList(self)
        return self
