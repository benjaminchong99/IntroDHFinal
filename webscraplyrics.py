import requests
from bs4 import BeautifulSoup

url = "https://www.azlyrics.com/"
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")

songrequest_dic = {}

songrequest = input("enter songs to search for lyrics, else press enter")
if songrequest == "":
    print("Ended boo")
else:
    # do sth
    pass
