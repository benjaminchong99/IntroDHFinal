# Code with reference to https://github.com/metalcorebear/NRCLex
from operator import length_hint
import matplotlib.pyplot as plt
import numpy as np
#import plotly.express as px
import pandas as pd
import re
# from nrclex import NRCLeximport as nltk
# nltk.download('punkt')
# nltk.download('wordnet')
from textblob import TextBlob, Word, Blobber

from textblob import TextBlob
from collections import Counter
from json import load


def __build_word_affect__(self):
    '''
    Instantiates the following attributes:
        affect_list
        affect_dict
        raw_emotion_scores
        affect_frequencies
    '''
    affect_list = []
    affect_dict = {}
    affect_frequencies = Counter()
    lexicon_keys = self.__lexicon__.keys()
    for word in self.words:
        if word in lexicon_keys:
            affect_list.extend(self.__lexicon__[word])
            affect_dict.update({word: self.__lexicon__[word]})
    for word in affect_list:
        affect_frequencies[word] += 1
    sum_values = sum(affect_frequencies.values())
    affect_percent = {'fear': 0.0, 'anger': 0.0, 'anticipation': 0.0, 'trust': 0.0, 'surprise': 0.0, 'positive': 0.0,
                      'negative': 0.0, 'sadness': 0.0, 'disgust': 0.0, 'joy': 0.0}
    for key in affect_frequencies.keys():
        affect_percent.update(
            {key: float(affect_frequencies[key]) / float(sum_values)})
    self.affect_list = affect_list
    self.affect_dict = affect_dict
    self.raw_emotion_scores = dict(affect_frequencies)
    self.affect_frequencies = affect_percent


def top_emotions(self):
    '''
    top_emotions becomes a list of (emotion: str, score: float) with the highest score associated to the input text.
    '''
    emo_dict = self.affect_frequencies
    max_value = max(emo_dict.values())
    top_emotions = []
    for key in emo_dict.keys():
        if emo_dict[key] == max_value:
            top_emotions.append((key, max_value))
    self.top_emotions = top_emotions


class NRCLex:
    """Lexicon source is (C) 2016 National Research Council Canada (NRC) and library is for research purposes only.  Source: http://sentiment.nrc.ca/lexicons-for-research/"""

    def __init__(self, lexicon_file='nrc_en.json'):
        with open(lexicon_file, 'r') as json_file:
            self.__lexicon__ = load(json_file)

    def load_token_list(self, token_list):
        '''
        Load an already tokenized text (as a list of tokens) into the NRCLex object.
        This is for when you want to use NRCLex with a text that you prefer to tokenize and/or lemmatize yourself.
        Parameters:
            token_list (list): a list of utf-8 strings.
        Returns:
            No return
        '''
        self.text = ""
        self.words = token_list
        self.sentences = []
        __build_word_affect__(self)
        top_emotions(self)

    def load_raw_text(self, text):
        '''
        Load a string into the NRCLex object for tokenization and lemmatization with TextBlob.
        Parameters:
            text (str): a utf-8 string.
        Returns:
            No return
        '''
        self.text = text
        blob = TextBlob(self.text)
        self.words = [w.lemmatize() for w in blob.words]
        self.sentences = list(blob.sentences)
        __build_word_affect__(self)
        top_emotions(self)


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
    # plt.legend(["lyrics", ""])
    plt.show()


"""START OF CODE"""

text_object = NRCLex(lexicon_file='nrc_en.json')


# to read the songs
with open("selectedsongsrock.txt", 'r') as f:
    lyrics = f.read()
    datas = lyrics.split("__Title__")

# print(datas)
newdata = []
for lines in datas:
    newline = lines.replace("\n", " ")
    if(lines != ''):
        newdata.append(newline)
# print(newdata)
rows_list = []
title_list = []
for num in range(len(newdata)):
    if(num % 2 == 0):
        if(newdata[num] != ''):
            title_list.append(newdata[num])
    else:
        text_object = NRCLex(lexicon_file='nrc_en.json')
        text_object.load_raw_text(newdata[num])
        res = text_object.affect_frequencies
        #res['total emotion score']=sum(text_object.raw_emotion_scores.values())
        #res['no.of words']=len(text_object.words)
        rows_list.append(res)

# print(title_list)
# print(len(title_list))
header = ["anger", "disgust", "fear", "negative", "sadness",
          "anticipation", "positive", "trust", "surprise", "joy"]

df = pd.DataFrame(rows_list, index=title_list, columns=header)

# print(df)
# the 10 emotions selected
# print(display(df))
column_average = {}
for emotion in header:
    column_average[emotion] = (df[emotion].mean())

print(column_average)

'''
# iloc is the [row][col]
dictionary = {}
for rowindex in range(len(df.iloc[:])):
    dictionary[title_list[rowindex]] = df.iloc[rowindex][:].tolist()
'''

# print("the dictionary: ", dictionary)
consolidatedlist = []
for key, value in column_average.items():
    consolidatedlist.append(value)
makeRadarGraph("Indie", consolidatedlist)  # function call
