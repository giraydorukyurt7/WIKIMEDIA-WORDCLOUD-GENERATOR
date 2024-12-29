import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from internal_functions.textCleaner import textCleaner
from textblob import TextBlob
from wordcloud import WordCloud
from flask import Flask, request, jsonify, render_template 
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'internal_functions'))

if os.path.exists("static/barplot.png"):
        os.remove("static/barplot.png")
if os.path.exists("static/wordCloud.png"):
        os.remove("static/wordCloud.png")

# Read Dataset Dynamically
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Create Dataset Path
DATASET_PATH = os.path.join(BASE_DIR, '..', 'Dataset', 'wiki_data.csv')

# READ CSV
wikimedia_data = pd.read_csv(DATASET_PATH, index_col=False)
wikimedia_data.columns = ["index", "text"]
wikimedia_data.drop(columns="index", inplace=True)

df = wikimedia_data.copy()

app = Flask(__name__)


#print(df.head())
#print(df.columns)
#print(df.isnull().sum())
#print(df.size)
#
#print(df["text"][100])


df["text"] = textCleaner(df["text"], remove_html=False)
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

def getPage(pageNo=1, cleanPage=False):
    if not cleanPage:
        return wikimedia_data["text"][pageNo]
    else:
        return df["text"][pageNo]

#print(getPage(pageNo=100))
#print(getPage(pageNo=100,cleanPage=True))

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
def generateBarPlot(pageNo=1, isALL=False, minTF=2):
    if(isALL):
        tf = df["text"].apply(lambda x: pd.Series(x.split(" ")).value_counts()).sum(axis=0).reset_index()
    else:
        pageText = df["text"].iloc[pageNo]
        tf = pd.Series(pageText.split()).value_counts().reset_index()
    tf.columns = ["words","tf"]
    #Bar plot
    #fig, ax = plt.subplots()
    filtered_tf = tf[tf["tf"]>minTF]
    if filtered_tf.empty:
        print("No data available for the given filter criteria.")
        return
    ax = filtered_tf.plot.bar(x="words", y="tf")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=10)
    plt.savefig("WikiMedia_Text_Mining_NLP/static/barplot.png", format="png", bbox_inches="tight")
    #plt.close(fig)
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
    plt.savefig("WikiMedia_Text_Mining_NLP/static/wordCloud.png", format="png", bbox_inches="tight")


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

@app.route("/get-page", methods=["POST"])
def get_page():
    data = request.json
    pageNo = data.get("pageNo", 1)
    cleanPage = data.get("cleanPage", False)

    result = getPage(pageNo=pageNo, cleanPage=cleanPage) #Calls function
    return jsonify({"Page": result})

@app.route("/get-bar-plot", methods=["POST"])
def get_barplot():
    data = request.json
    pageNo = data.get("pageNo",1)
    isALL = data.get("isALL", False)
    minTF = data.get("minTF", 2)

    if os.path.exists("static/barplot.png"):
        os.remove("static/barplot.png")

    generateBarPlot(pageNo=pageNo, isALL=isALL, minTF=minTF)

    if not os.path.exists("WikiMedia_Text_Mining_NLP/static/barplot.png"):
        return jsonify({"success": False, "message": "No data available for the given filter criteria."})
    return jsonify({"success": True, "plotUrl":"/static/barplot.png"})

@app.route("/get-wordCloud", methods=["POST"])
def get_wordCloud():
    data = request.json
    pageNo = data.get("pageNo",1)
    isALL = data.get("isALL", False)

    if os.path.exists("static/wordCloud.png"):
        os.remove("static/wordCloud.png")

    generateWordCloud(pageNo=pageNo, isALL=isALL)

    if not os.path.exists("WikiMedia_Text_Mining_NLP/static/wordCloud.png"):
        return jsonify({"success": False, "message": "No data available for the given filter criteria."})
    return jsonify({"success": True, "plotUrl":"/static/wordCloud.png"})

if __name__ == "__main__":
    app.run(debug=True)