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
        songrequest = key
        artist = value

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
        else:
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
            if lyrics != "":
                songrequest_dic[f"{edited_songrequest} by {edited_artist}"] = lyrics

        # ending sequence
    # store lyrics in txt file
    with open('selectedsongsrock.txt', 'w') as f:
        indexing = 0
        for key, value in songrequest_dic.items():
            key = re.sub("-", " ", key)
            f.write(f"__Title__ " + key.title() + "\n")
            f.write('\n')
            f.write(value)
            f.write('\n')
            indexing += 1
    print("INDEX: ", indexing)
    return songrequest_dic


with open("rock.txt", 'r') as f:
    titles = f.read()
    titles = re.sub("\d+\\t", "", titles)
    filter = titles.split("\n")

    dict = {}
    for wordtgt in filter:
        temp = wordtgt.split("\t")
        print(temp)
        try:
            dict[temp[1]] = temp[0]
        except:
            print("skip this song")

print(dict)
# dictionary = {"paramore": "misery business",
#               "My Chemical Romance": "Helena",
#               "My Chemical romance": "I'm not okay",
#               "Blink 182": "I miss you",
#               "The Red JumpSuit Apparatus": "Face Down",
#               "Fall out Boy": "Thnks fr th Mmrs",
#               "Good charlotte": "the anthem",
#               "Linkin Park": "numb",
#               "YellowCard": "Ocean Avenue",
#               "Mayday parade": "Miserable at best",
#               "Sleeping with sirens": "If you can't hang",
#               "blink 182": "First Date",
#               "Sum41": "In too deep",
#               "bring me the horizon": "throne",
#               "Bullet For my valentine": "Tears Don't Fall",
#               "Mayday Parade": "Jamie All Over",
#               "my Chemical Romance": "Welcome to the Black Parade",
#               "Pierce the Veil": "King for a day",
#               "All Time Low": "Therapy",
#               "Simple Plan": "Perfect",
#               "We the Kings": "Skyway Avenue",
#               "The Killers": "Mr Brightside"
#               }

findlyrics(dict)
