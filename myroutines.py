import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer


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