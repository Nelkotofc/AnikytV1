from __init__ import *


class Anilist:
    def __init__(self, accID, accessToken, acctJson, userJson):
        # accID : 11791 (https://anilist.co/settings/developer: Anilist API Client Id)
        # accessToken : Fonction to get Token
        self.accID = accID
        self.accessToken = accessToken

        # acctJson : accounts.json
        self.userJson = userJson
        self.acctJson = acctJson
        self.accounts = {}
        self.aniAccounts = {}
        self.user = None

    def getTokenPage(self):
        return f'https://anilist.co/api/v2/oauth/authorize?client_id={self.accID}&response_type=token'

    def login(self, account):
        if account.verified:
            self.user = account.login()
        else:
            quit("Account not verified")

    def save_user(self):
        with open(self.userJson, 'w') as f:
            json.dump(self.user.username, f)

    def save_account(self):
        with open(self.acctJson, 'w') as f:
            json.dump(self.accounts, f)

    def load_user(self):
        with open(self.userJson, 'r') as f:
            userName = json.load(f)
            if userName is not None:
                self.user = self.aniAccounts.get(userName)


    def load_accounts(self):
        with open(self.acctJson, 'r') as f:
            self.accounts = json.load(f)

        for account in list(self.accounts.keys()):
            Anc = AniAccount(account)
            Anc.verified = True
            Anc.information = self.accounts[account][0]
            Anc.token = self.accounts[account][1]
            self.aniAccounts[Anc.username] = Anc
            Anc.login()
