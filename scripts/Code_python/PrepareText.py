import pandas as pd
import re
import nltk
from sklearn.feature_extraction.text import CountVectorizer
import string


def remove_punct(df, columns):
    for column in columns:
        df[column] = df[column].apply(lambda x: re.sub(r'[^\w\s-]', '', x))
        df[column] = df[column].apply(lambda x: re.sub(r'&*#\d*', '', x))
        #TODO investigate ;s
    return df

def remove_whitespace(df, columns):
    for column in columns:
        df[column] = df[column].apply(lambda x: x.strip())
        df[column] = df[column].apply(lambda x: re.sub(r'((?<![\d\s])\s\s+(?=\w))', r' ', x))
    return df

def lower_case(df, columns):
    for column in columns:
        df[column] = df[column].apply(lambda x: x.lower())
    return df

def add_spaces(df, columns):
    for column in columns:
        df[column] = df[column].apply(lambda x: re.sub(r'([.a-z](?=[A-Z]))', r'\1 ', x))
        df[column] = df[column].apply(lambda x: re.sub(r'((?<=\d)[a-zA-Z])', r' \1', x))
    return df

def change_numbers(df,columns):
    for column in columns:
        df[column] = df[column].apply(lambda x: re.sub(r'[-+]?\d+\s*\.?\d*', 'num', x))
    return df

def tokenize(text):
    tokens = re.split(r'\W+', text)
    return tokens

def remove_stopwords(tokenized_list):
    return [word for word in tokenized_list if word not in nltk.corpus.stopwords.words("english")]

def analyze_words(tokenized_lemm_list, words):
    analyze_dict = {}
    for i, word in enumerate(tokenized_lemm_list):
        bef_aft = []
        if word in words:
            bef_aft.append(words[i-1])
            bef_aft.append(words[i+1])



def lemmitize_text(tokenized_list):
    wn = nltk.WordNetLemmatizer()
    return [wn.lemmatize(word) for word in tokenized_list]

def stem_text(tokenized_list):
    ps = nltk.PorterStemmer()
    return [ps.stem(word) for word in tokenized_list]

def clean_text_stem(text):
        tokens = remove_stopwords(tokenize(text))
        return stem_text(tokens)

def clean_text_lemm(text):
    tokens = remove_stopwords(tokenize(text))
    return lemmitize_text(tokens)


def main():
    raw_text = pd.read_csv("..\\..\\data\\derived\\raw_text_with_datetime_manual.csv",
                           encoding="cp1252", parse_dates=[["date", "time"]])

    raw_text = add_spaces(raw_text, ["text"])
    raw_text = remove_punct(raw_text, ["text"])
    raw_text = remove_whitespace(raw_text, ["text"])
    raw_text = lower_case(raw_text, ["text"])
    raw_text = change_numbers(raw_text, ["text"])

    # print(raw_text.to_string())

    # raw_text["text_tokenized"] = raw_text["text"].apply(lambda x : tokenize(x))
    # raw_text["text_nostop"] = raw_text["text_tokenized"].apply(lambda x: remove_stopwords(x))
    # raw_text["text_stemmed"] = raw_text["text_nostop"].apply(lambda x: stem_text(x))
    # raw_text["text_lemm"] = raw_text["text_nostop"].apply(lambda x: lemmitize_text(x))



    # print(raw_text["text_lemm"].apply(lambda x: len(x)).to_string())
    # print(raw_text["text_stemmed"].apply(lambda x: len(x)).to_string())

    vectorizer = CountVectorizer(analyzer=clean_text_lemm, min_df=.75)
    X_counts = vectorizer.fit_transform(raw_text["text"])
    print("X_counts1_lemm", X_counts.shape)
    print("X_counts_lemm_num_words", vectorizer.get_feature_names())
    # print(vectorizer.inverse_transform(raw_text["text"]))
    # print(X_counts.toarray())


    # vectorizer = CountVectorizer(analyzer=clean_text_stem, min_df=.75)
    # X_counts2 = vectorizer.fit_transform(raw_text["text"])
    # print("X_Counts2_stemmed", X_counts2.shape)
    # print("X_counts2_stemmed_words", vectorizer.get_feature_names())


if __name__ == '__main__':
    main()