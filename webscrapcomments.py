import time
import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np

def get_comments(link):
    data=[]
    with Chrome(executable_path=r'C:\Users\User\Documents\Dh\chromedriver.exe') as driver:
        wait = WebDriverWait(driver,15)
        driver.get(link)

        for item in range(3): 
            wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
            time.sleep(5)

        for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content"))):
            data.append(comment.text)
            print(comment.text)
            
    return data

from nrclex_trial1 import*
#nrc per DH_NRClex

def one_song(title, artist, comments_list):
    # takes in list of comments
    # takes in title of song: artist song
    # returns one dictionary line to be added to list
    
    comments_list = comments_list[4:]
    df_comments = pd.DataFrame(comments_list, columns=["comment"])
    
    text_object = NRCLex(lexicon_file='nrc_en.json')
    
    nrc_d_list=[]
    # code sample taken from varshini's code in menu
    for j in range(df_comments.shape[0]):
        
        comment = df_comments["comment"].iloc[j]
        text_object.load_raw_text(comment)
        res=text_object.affect_frequencies
        nrc_d_list.append(res)
        #print(j, res)
    
    
    column_names = ["fear","anger","anticipation","trust","surprise","positive","negative","sadness","disgust","joy"]
    # get average
    df=pd.DataFrame(nrc_d_list, columns=column_names)
    #print(display(df))
    column_average = {"title": title, "artist": artist}
    for column_name in column_names:
        column_average[column_name] = (df[column_name].mean())
    
    #print(column_average)
    return column_average

#data into comments body
def nrc_per_genre(df_in):
    
    df_copy = df_in
    df_out = pd.DataFrame(np.zeros((1, 10)))
    d_all = {'title':[],
             'artist':[],
             'comments':[],
             'url':[]}
    
    genre_nrc_songlist = []
    for i in range(df_in.shape[0]):
        print("start, ", i)
        artist = df_copy["first_artist"].iloc[i]
        title = df_copy["title"].iloc[i]
        genre = df_copy["genre"].iloc[i]
        url = df_copy["url"].iloc[i]
        
        if url != "NA":
            # scrap data from youtube of one song
            comments_list = get_comments(url)
            for comments in comments_list:
                d_all['title'].append(title)
                d_all['artist'].append(artist)
                d_all['comments'].append(comments)
                d_all['url'].append(url)
            
            genre_nrc_songlist.append(one_song(title, artist, comments_list))
            print("end, ", i)
    
    #print(df_comments)
    df_comments = pd.DataFrame(d_all, columns=['title','artist','comments','url'])
    df_comments.to_csv(f'DH_{genre}_comments2.csv', index=False)
    #print(genre_nrc_songlist)
    
    df_out = pd.DataFrame(genre_nrc_songlist)
    df_out.to_csv(f'DH_{genre}_nrcparsed2.csv', index=False)
    
    #make visualisations
    avg_d = getAvg_df(df_out)
    for key, value in avg_d.items():
            makeRadarGraph(key, value)  # function call

    return df_out
    
# # Make Diagrams

from operator import length_hint
import matplotlib.pyplot as plt
import numpy as np
#import plotly.express as px
import pandas as pd

def getAvg_df(df):
    column_names = ["fear","anger","anticipation","trust","surprise","positive","negative","sadness","disgust","joy"]
    column_average = {}
    for column_name in column_names:
        column_average[column_name] = (df[column_name].mean())
        
    return column_average

def makeRadarGraph(key, values):

    # the 10 emotions selected
    header = ["anger", "disgust", "fear", "negative", "sadness",
              "anticipation", "positive", "trust", "surprise", "joy"]

    # Split the circle into even parts and save the angles
    # so we know where to put each axis.
    angles = np.linspace(0, 2 * np.pi, 10, endpoint=False).tolist()

    # The plot is a circle, so we need to "complete the loop"
    # and append the start value to the end.
    values += values[:1]
    angles += angles[:1]

    # ax = plt.subplot(polar=True)
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    # Draw the outline of our data.
    ax.plot(angles, values, color='red', linewidth=1)
    # ax.plot(angles, values1, color='orange', linewidth=1)
    # Fill it in.
    ax.fill(angles, values, color='red', alpha=0.25, )
    # ax.fill(angles, values1, color='orange', alpha=0.25)

    # Fix axis to go in the right order and start at 12 o'clock.
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    # Draw axis lines for each angle and label.
    ax.set_thetagrids(np.degrees(angles[:-1]), header)

    # Go through labels and adjust alignment based on where
    # it is in the circle.
    for label, angle in zip(ax.get_xticklabels(), angles):
        if angle in (0, np.pi):
            label.set_horizontalalignment('center')
        elif 0 < angle < np.pi:
            label.set_horizontalalignment('left')
        else:
            label.set_horizontalalignment('right')
    plt.title(key, size=20)
    #plt.legend(["lyrics", ""])
    plt.show()

df = pd.read_csv (r'DH_country.csv')
#nrc_per_genre(df, test_comments_store)
nrc_per_genre(df)
#print (df)


df = pd.read_csv (r'DH_indie2.csv')
#nrc_per_genre(df, test_comments_store)
nrc_per_genre(df)
#print (df)


df = pd.read_csv (r'DH_rock.csv')
#nrc_per_genre(df, test_comments_store)
nrc_per_genre(df)
#print (df)


df = pd.read_csv (r'DH_indie2_nrcparsed2.csv')
#print(display(df))
avg_d = getAvg_df(df)
print(avg_d)
values = [avg_d["anger"], avg_d["disgust"], avg_d["fear"], avg_d["negative"], avg_d["sadness"],
              avg_d["anticipation"], avg_d["positive"], avg_d["trust"], avg_d["surprise"], avg_d["joy"]]

makeRadarGraph("Indie", values)  # function call


df = pd.read_csv (r'DH_rock_nrcparsed2.csv')
#print(display(df))
avg_d = getAvg_df(df)
print(avg_d)
values = [avg_d["anger"], avg_d["disgust"], avg_d["fear"], avg_d["negative"], avg_d["sadness"],
              avg_d["anticipation"], avg_d["positive"], avg_d["trust"], avg_d["surprise"], avg_d["joy"]]

makeRadarGraph("Rock", values)  # function call


df = pd.read_csv (r'DH_country_nrcparsed2.csv')
#print(display(df))
avg_d = getAvg_df(df)
print(avg_d)
values = [avg_d["anger"], avg_d["disgust"], avg_d["fear"], avg_d["negative"], avg_d["sadness"],
              avg_d["anticipation"], avg_d["positive"], avg_d["trust"], avg_d["surprise"], avg_d["joy"]]

makeRadarGraph("Country", values)  # function call


