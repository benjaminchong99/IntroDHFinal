import requests
import re
from bs4 import BeautifulSoup

# url = "https://www.azlyrics.com/"
# url = "https://www.songlyrics.com/ed-sheeran/shape-of-you-lyrics/"
# r = requests.get(url)
# soup = BeautifulSoup(r.text, "html.parser")
# results = soup.find(id="songLyricsDiv")
# print(results)


def findlyrics():
    songrequest_dic = {}

    songrequest = input("Enter songs to search for lyrics, else press enter")
    while songrequest != "":
        if songrequest == "0.0":
            # store lyrics in txt file
            with open('selectedsongs.txt', 'w') as f:
                for key, value in songrequest_dic.items():
                    f.write(key + "\n")
                    f.write(value)
                    f.write('\n')
            return songrequest_dic
        # search for the song using track name and artist name
        edited_songrequest = songrequest.lower()
        edited_songrequest = re.sub(" ", "-", edited_songrequest)
        artist = input("Enter artist of the song")
        edited_artist = artist.lower()
        edited_artist = re.sub(" ", "-", edited_artist)
        print(edited_songrequest, edited_artist)

        # start to search for the song below
        url = f"https://www.songlyrics.com/{edited_songrequest}/{edited_artist}-lyrics/"
        print(url)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        results = soup.find(id="songLyricsDiv")
        results = str(results)
        print("Results: ", results)
        if results.__contains__("Sorry, we have no"):
            print("error")
            break

        initialgrab = re.findall(">[\w\s,!']+", results)
        finalgrab = []
        for clause in initialgrab:
            clause = re.sub("[>\n]", "", clause)
            if clause != "":
                finalgrab.append(clause)
        lyrics = ""
        for line in finalgrab:
            lyrics += line + "\n "
        songrequest_dic[f"{edited_songrequest} by {edited_artist}"] = lyrics

        # ending sequence
        songrequest = input(
            "Enter songs to search for lyrics, else press enter")
    print("Ended boo")


findlyrics()
