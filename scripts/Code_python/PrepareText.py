import pandas as pd
import re
import string


def remove_punct(df, columns):
    for column in columns:
        df[column] = df[column].apply(lambda x: re.sub(r'[^\w\s-]', '', x))
        df[column] = df[column].apply(lambda x: re.sub(r'&*#\d*', '', x))
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

def main():
    raw_text = pd.read_csv("..\\..\\data\\derived\\raw_text_with_datetime_manual.csv",
                           encoding="cp1252", parse_dates=[["date", "time"]])

    raw_text = add_spaces(raw_text, ["text"])
    raw_text = remove_punct(raw_text, ["text"])
    raw_text = remove_whitespace(raw_text, ["text"])
    raw_text = lower_case(raw_text, ["text"])


    print(raw_text.to_string())

if __name__ == '__main__':
    main()