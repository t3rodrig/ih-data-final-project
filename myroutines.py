import re
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


def clean_up(s, stop_words=stopwords.words('spanish'), stemmer=SnowballStemmer("spanish", ignore_stopwords=True)):
    word_list = s.lower().split(" ")
    word_list = [re.sub(r'\d', ' ', word) for word in word_list]
    word_list = [re.sub(r'\W', ' ', word) for word in word_list]
    new_string = " ".join(word_list)

    token_list = word_tokenize(new_string)
    stem_list=[stemmer.stem(token) for token in token_list]
    new_list = [token for token in stem_list if token not in stop_words]
    new_string = " ".join(new_list)
    return new_string

# Function that takes a description as input and outputs most similar product
def get_recommendation(description, text_series, df):
    description = clean_up(description)
    tmp_series = pd.concat([
        text_series,
        pd.Series([description])
    ], ignore_index=True)

    vectorizer = TfidfVectorizer(
        analyzer='word',
        ngram_range=(1, 2),
        min_df=0.003
    )
    
    #Construct the required TF-IDF matrix by fitting and transforming the data
    tfidf_matrix = vectorizer.fit_transform(tmp_series)

    # Compute the cosine similarity matrix
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    
    # Set the index of product description
    idx = -1
    
    # Get the pairwsie similarity scores of all products with that product
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    # Sort the products based on the scores
    sim_scores = sorted(sim_scores, key=lambda x:x[1], reverse=True)
    
    # Get the score of the 10 most similar products
    sim_scores = sim_scores[1:11]
    
    # Get the product indices
    product_indices = [i[0] for i in sim_scores]
    
    # Return  the top most similar products
    return df.iloc[product_indices]