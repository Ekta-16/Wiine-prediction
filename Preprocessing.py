import csv

import pandas as pd
import re

from nltk.corpus import stopwords
import nltk
import nltk as nlp
nltk.download("punkt")
nltk.download("wordnet")
nltk.download("stopwords")


def preprocess():
    # Reading the csv file
    df = pd.read_csv(r'New_wine.csv')
    print(df)
    # Total dataset
    print("Length of dataframe before duplicates are removed:", len(df))
    df.head()

    # Total Number of the null values in each attribute
    null_columns = df.columns[df.isnull().any()]
    total = df[null_columns].isnull().sum()
    print(total)

    # Total percentage of the null values in each attribute
    percent = (df.isnull().sum() / df.isnull().count() * 100).sort_values(ascending=False)
    print(percent)

    print (df[df.duplicated('description', keep=False)].sort_values('description').head(5))
    print(df.shape)

    df = df.drop_duplicates('description')
    print (df.shape)

    meanPoints = df.points.mean()
    df["Above_Average"] = [1 if i > meanPoints else 0 for i in df.points]

    allRecords = []

    lemma = nlp.WordNetLemmatizer()
    for i, record in df.iterrows():
        description = record['description']
        point = record['points']
        # Using regex to delete non-alphabetic characters on data.
        description = re.sub("[^a-zA-Z]", " ", description)
        # turn upper, lower and whole characters into lowercase.
        description = description.lower()
        # tokenizing the description statement
        description = nltk.word_tokenize(description)
        # Removing stop words like 'the', 'or', 'and', 'is' etc.
        description = [i for i in description if i not in set(stopwords.words("english"))]
        #  Performing lemmatization for e.g: giving => give
        description = [lemma.lemmatize(i)for i in description]
        # Turning words list into sentence again
        description = " ".join(description)
        #printing the description
        # print(description)
        allRecords.append({'point': point, 'des': description})
    return allRecords


if __name__ == '__main__':
    data = preprocess()
    keys = data[0].keys()
    with open('preprocessed.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

