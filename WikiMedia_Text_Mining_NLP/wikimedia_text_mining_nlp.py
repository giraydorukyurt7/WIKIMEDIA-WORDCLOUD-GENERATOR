import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from internal_functions.textCleaner import textCleaner
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