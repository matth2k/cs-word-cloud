from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
import random
import re
import string

from wordcloud import WordCloud, STOPWORDS

imageHeight = 0

slurs = ["faggot", "nigger", "chink", "spic", "retard", "retarded", "nig", "gay"]
swears = ["fuck", "shit", "damn", "fucking", "shitting"]
colorDict = {
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "purple": (128, 0, 128),
    "orange": (255, 165, 0),
}

russianWords = ["беше", "моука"]


def grey_color_func(
    word, font_size, position, orientation, random_state=None, **kwargs
):
    orange = (235, 164, 52)
    grey = (163, 163, 163)
    noiseScale = 16
    noise = (
        random.randint(-noiseScale, noiseScale),
        random.randint(-noiseScale, noiseScale),
        random.randint(-noiseScale, noiseScale),
    )
    color = None
    pPosition = position[0] / imageHeight
    probability = None
    if pPosition > 0.33:
        probability = 0.5 + 0.5 * (position[0] - imageHeight / 3.0) / (
            2.0 * imageHeight / 3.0
        )
    else:
        probability = 0.5 - 0.5 * (
            ((imageHeight / 3.0) - position[0]) / (imageHeight / 3.0)
        )
    colorChoice = random.choices(
        [orange, grey], weights=[probability, 1.0 - probability], k=1
    )[0]

    color = (
        max(0, min(255, noise[0] + colorChoice[0])),
        max(0, min(255, noise[1] + colorChoice[1])),
        max(0, min(255, noise[2] + colorChoice[2])),
    )
    brightness = 0.5

    if word in slurs:
        color = (
            max(0, min(255, int(brightness * color[0]))),
            max(0, min(255, int(brightness * color[1]))),
            max(0, min(255, int(brightness * color[2]))),
        )
        color = (255, 0, 0)

    elif word in swears:
        color = (
            max(0, min(255, int(brightness * color[0]))),
            max(0, min(255, int(brightness * color[1]))),
            max(0, min(255, int(brightness * color[2]))),
        )
    elif word in colorDict:
        color = colorDict[word]

    return f"rgb({color[0]}, {color[1]}, {color[2]})"


# get data directory (using getcwd() is needed to support running example in generated IPython notebook)
d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

# Read the whole text.
text = open(path.join(d, "words.txt")).read()
filteredText = ""
if True:
    for i in text:
        if not re.findall("[^a-zA-Z\d\s:]", i):
            filteredText += i

print(filteredText)

# read the mask image
# taken from
# http://www.stencilry.org/stencils/movies/alice%20in%20wonderland/255fk.jpg
alice_mask = np.array(Image.open(path.join(d, "csgo_mask.jpg")))
imageHeight = alice_mask.shape[0]

stopwords = set(STOPWORDS)
stopwords.add("said")
stopwords.add("ready")
stopwords.add("unpause")
stopwords.add("need")
stopwords.add("gaben")
stopwords.add("an")
stopwords.add("a")
stopwords.add("of")
stopwords.add("that")
stopwords.add("but")
stopwords.add("can")
stopwords.add("on")
stopwords.add("for")
stopwords.add("to")
stopwords.add("switch")
stopwords.add("stay")
stopwords.add("pause")
stopwords.add("krajliwtf")
stopwords.add("pitou")
stopwords.add("zycsell")
stopwords.add("co")
for l in string.ascii_lowercase:
    stopwords.add(l)

wc = WordCloud(
    background_color="white",
    max_words=200,
    mask=alice_mask,
    stopwords=stopwords,
    contour_width=0,
    margin=5,
    contour_color="navy",
    relative_scaling=0.46,
    collocations=False,
    prefer_horizontal=0.66,
)

# generate word cloud
wc.generate(filteredText)
wc.recolor(color_func=grey_color_func, random_state=3)

# store to file
wc.to_file(path.join(d, "csgo_word_cloud.png"))

# What are CS players saying? Here's a word cloud of the most common words in game chat.
