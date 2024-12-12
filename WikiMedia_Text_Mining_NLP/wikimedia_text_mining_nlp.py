import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from internal_functions.textCleaner import textCleaner
from textblob import TextBlob
from wordcloud import WordCloud
from flask import Flask, request, jsonify, render_template 
import sys
sys.stdout.reconfigure(encoding='utf-8')

wikimedia_data = pd.read_csv("Dataset/wiki_data.csv", index_col=False)
wikimedia_data.columns = ["index","text"]
wikimedia_data.drop(columns="index",inplace=True)

df = wikimedia_data.copy()

app = Flask(__name__)


#print(df.head())
#print(df.columns)
#print(df.isnull().sum())
#print(df.size)
#
#print(df["text"][100])

#df["text"] = textCleaner(df["text"], remove_html=False)
#print("============\n\n\n")
#print(df["text"][100])
#checking with tokenization
#print(df["text"].apply(lambda x: TextBlob(x).words).head())

def generateTitle(pageNo=1, isALL=False, titleSize=3):
    if(isALL):
        title = "WikiMedia"
    else:
        title = " ".join(wikimedia_data.loc[pageNo, "text"].split()[:titleSize])
    return title

#print(generateTitle(isALL=True))
#print(generateTitle(pageNo=100))



##term frequency
#tf = df["text"].apply(lambda x: pd.Series(x.split(" ")).value_counts()).sum(axis=0).reset_index()
#print(tf.head())
#tf.columns = ["words","tf"]
#print(tf)
#
##Bar plot
#ax = tf[tf["tf"]>200].plot.bar(x="words", y="tf")
#ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=10)
#plt.tight_layout()
#plt.show()

##Bar Plot For Every Text
def generateBarPlot(pageNo=1, isALL=False, minTF=200):
    if(isALL):
        tf = df["text"].apply(lambda x: pd.Series(x.split(" ")).value_counts()).sum(axis=0).reset_index()
        minTF=2000
    else:
        pageText = df["text"].iloc[pageNo]
        tf = pd.Series(pageText.split()).value_counts().reset_index()
    tf.columns = ["words","tf"]
    #Bar plot
    ax = tf[tf["tf"]>minTF].plot.bar(x="words", y="tf")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=10)
    plt.tight_layout()
    plt.show()

#generateBarPlot(pageNo=100, minTF=1)

#generateBarPlot(isALL=True)


#Word Cloud For Every Text
def generateWordCloud(pageNo=1, isALL=False):
    if(isALL):
        text = " ".join(i for i in df.text)
        generateThis = text
    else:
        generateThis = df["text"][pageNo]

    wordcloud = WordCloud(background_color="lightgray",
                          max_words=1000,
                          contour_width=3,
                          contour_color="firebrick",
                          colormap="gist_rainbow",
                          width=8000,
                          height=4000).generate(generateThis)
    plt.figure(figsize=(20,10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()


#generateWordCloud(pageNo=100)

#generateWordCloud(isALL=True)





@app.route("/")
def index(): #renders the page
    return render_template("WikiMedia_World_Cloud.html")

@app.route("/generate-title", methods=["POST"])
def get_title():
    data = request.json
    pageNo = data.get("pageNo", 1)
    isALL = data.get("isALL", False)
    titleSize = data.get("titleSize", 3)

    result = generateTitle(pageNo=pageNo, isALL=isALL, titleSize=titleSize) #Calls function
    return jsonify({"title": result})

if __name__ == "__main__":
    app.run(debug=True)