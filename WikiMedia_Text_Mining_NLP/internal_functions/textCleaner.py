import pandas as pd
import nltk
from bs4         import BeautifulSoup
from nltk.corpus import stopwords
from textblob    import Word

#IMPORTANT: Download these packages before use
#nltk.download('stopwords')     # --> Text Preprocessing
#nltk.download('wordnet')       # --> Text Preprocessing

# Note: if you want to use this code the dataframe shouldn't have null values.
# Example for handling null values:
# df = df.dropna(subset="Review")
def textCleaner(df_text, remove_html=True, rare_words = True):
    # Remove html elements
    if remove_html:
        df_text = df_text.apply(lambda x: ' '.join(BeautifulSoup(str(x), "html.parser").get_text().split()) if pd.notnull(x) else x)
    # lowerCase transformation
    df_text = df_text.str.lower()
    # Remove punctions
    df_text = df_text.str.replace(r'[^\w\s]', ' ', regex=True)
    # Remove Numbers
    df_text = df_text.str.replace(r'\d+', " ", regex=True)
    # Remove Stopwords
    sw = stopwords.words('english')
    df_text = df_text.apply(lambda x: " ".join(x for x in str(x).split() if x not in sw))
    # Remove Rarewords
    if rare_words:
        rarewords_df = pd.Series(' '.join(df_text).split()).value_counts()
        drops = rarewords_df[rarewords_df<=2]
        df_text = df_text.apply(lambda x: " ".join(x for x in str(x).split() if x not in drops))
    # Lemmatization
    df_text = df_text.apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))
    # Remove Extra Spaces
    df_text = df_text.str.replace(r'\s+', ' ', regex=True)
    return df_text