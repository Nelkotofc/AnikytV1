from __init__ import *


def run():
    manager = Manager(accID=11791,
                      acctJson="Datas\\accounts.json",
                      userJson="Datas\\user.json",
                      WindowTitle="Anikyt", WindowSize=(1280, 720),
                      WindowIcon="Ressources\logo.jpg",
                      DisplayColor="white", romaji=False, DisplayModel="list", AdultMedias=False, ModelSize="small", AllModel=False, CustomModel=True) # AdultMedias is reversed (False for adult medias)


if __name__ == "__main__":
    run()
