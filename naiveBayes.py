import json
import pandas

data = pandas.read_csv("preprocessed.csv")
frequency = {}

trainingData = data.sample(frac=0.7)
testing = data.drop(trainingData.index).to_csv(r'testset.csv', index=False)
setOfWords = set()


def process():
    totalRecords = 0
    # goes through all the rows and calculates the total occurrence of each word for all points
    for i, record in trainingData.iterrows():
        totalRecords += 1
        des = record['des'].split(' ')
        point = record['point']
        if point not in frequency:
            frequency[point] = {'wordsFrequency': {}, 'totalRows': 0, 'totalWords': 0}
        frequency[point]['totalRows'] += 1
        for word in des:
            setOfWords.add(word)
            if word not in frequency[point]['wordsFrequency']:
                frequency[point]['wordsFrequency'][word] = 1
            frequency[point]['wordsFrequency'][word] += 1
            frequency[point]['totalWords'] += 1
    # remove the words that have less occurrence
    # for point in frequency.keys():
    #     words = frequency[point]['wordsFrequency']
    #     totalRows = frequency[point]['totalRows']
    #     newWords = {k: v for k, v in words.items() if (v > (totalRows*0.01))}
    #     frequency[point]['wordsFrequency'] = newWords
    frequency['totalRecords'] = totalRecords
    frequency['setOfWords'] = list(setOfWords)
    with open('frequency.json', 'w') as f:
        f.write(json.dumps(frequency))
        f.close()


if __name__ == '__main__':
    process()
