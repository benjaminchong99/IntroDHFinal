import requests
import re
from bs4 import BeautifulSoup

# url = "https://www.azlyrics.com/"
# url = "https://www.songlyrics.com/ed-sheeran/shape-of-you-lyrics/"
# r = requests.get(url)
# soup = BeautifulSoup(r.text, "html.parser")
# results = soup.find(id="songLyricsDiv")
# print(results)


def findlyrics(dictionary):
    songrequest_dic = {}
    for key, value in dictionary.items():
        songrequest = value
        artist = key

        # search for the song using track name and artist name
        edited_songrequest = songrequest.lower()
        edited_songrequest = re.sub(" ", "-", edited_songrequest)
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
        # scraping with regex
        initialgrab = re.findall(">[\w\s,!'â€~]+", results)
        print("Initialgrab: ", initialgrab)
        finalgrab = []
        for clause in initialgrab:
            clause = re.sub("[>\nâ€~]", "", clause)
            print("Clause: ", clause)
            if clause != "":
                finalgrab.append(clause)
        lyrics = ""
        for line in finalgrab:
            lyrics += line + "\n "
        songrequest_dic[f"{edited_songrequest} by {edited_artist}"] = lyrics

        # ending sequence
    # store lyrics in txt file
    with open('selectedsongs.txt', 'w') as f:
        for key, value in songrequest_dic.items():
            key = re.sub("-", " ", key)
            f.write(key.title() + "\n")
            f.write('\n')
            f.write(value)
            f.write('\n')
    print("Ended boo")
    return songrequest_dic


dictionary = {"paramore": "misery business",
              "My Chemical Romance": "Helena",
              "My Chemical romance": "I'm not okay",
              "Blink 182": "I miss you",
              "The Red JumpSuit Apparatus": "Face Down",
              "Fall out Boy": "Thnks fr th Mmrs",
              "Good charlotte": "the anthem",
              "Linkin Park": "numb",
              "YellowCard": "Ocean Avenue",
              "Mayday parade": "Miserable at best",
              "Sleeping with sirens": "If you can't hang",
              "blink 182": "First Date",
              "Sum41": "In too deep",
              "bring me the horizon": "throne",
              "Bullet For my valentine": "Tears Don't Fall",
              "Mayday Parade": "Jamie All Over",
              "my Chemical Romance": "Welcome to the Black Parade",
              "Pierce the Veil": "King for a day",
              "All Time Low": "Therapy",
              "Simple Plan": "Perfect",
              "We the Kings": "Skyway Avenue",
              "The Killers": "Mr Brightside"
              }

findlyrics(dictionary)
