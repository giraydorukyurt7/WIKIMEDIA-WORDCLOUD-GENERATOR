import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from internal_functions.textCleaner import textCleaner
from textblob import TextBlob
from wordcloud import WordCloud
import sys
sys.stdout.reconfigure(encoding='utf-8')

wikimedia_data = pd.read_csv("Dataset/wiki_data.csv", index_col=False)
df = wikimedia_data.copy()
df.columns = ["index","text"]
df.drop(columns="index",inplace=True)
print(df.head())
print(df.columns)
print(df.isnull().sum())
print(df.size)

print(df["text"][100])
df["text"] = textCleaner(df["text"], remove_html=False)
print("============\n\n\n")
print(df["text"][100])
#checking with tokenization
#print(df["text"].apply(lambda x: TextBlob(x).words).head())

#term frequency
tf = df["text"].apply(lambda x: pd.Series(x.split(" ")).value_counts()).sum(axis=0).reset_index()
tf.columns = ["words","tf"]
print(tf)

#Bar plot
ax = tf[tf["tf"]>200].plot.bar(x="words", y="tf")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=10)
plt.tight_layout()
plt.show()

#Word Cloud
text = " ".join(i for i in df.text)
wordcloud = WordCloud(background_color="lightgray",
                      max_words=1000,
                      contour_width=3,
                      contour_color="firebrick",
                      colormap="gist_rainbow",
                      width=8000,
                      height=4000).generate(text)
plt.figure(figsize=(20,10))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()