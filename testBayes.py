import pandas
import json

df = pandas.read_csv('testset.csv')
frequency = json.loads(open('frequency.json').read())
setOfWords = frequency['setOfWords']


def predictPoint(des):
    des = des.split(' ')
    probabilities = {}
    totalRecords = frequency['totalRecords']
    for point in range(80, 101):
        point = str(point)
        probA = frequency[point]['totalRows']/totalRecords
        wordsForThisPoint = frequency[point]['wordsFrequency']
        prob = 1
        for word in des:
            if word in wordsForThisPoint.keys():
                prob *= (wordsForThisPoint[word]/(frequency[point]['totalWords'] + len(setOfWords)))
            else:
                prob *= (1/(frequency[point]['totalWords'] + len(setOfWords)))
        prob *= probA
        probabilities[point] = prob

    probabilities = [k for k, v in sorted(probabilities.items(), key=lambda item: item[1], reverse=True)]
    return probabilities


def test():
    count = 0
    total = 0
    print("Testing the algorithm...")
    for i, record in df.iterrows():
        des = record['des']
        point = record['point']
        point2 = predictPoint(des)[0]
        if abs(int(point2) - int(point)) < 3:
            count += 1
        total += 1

    return total, count

if __name__ == '__main__':
    total, count = test()
    print('Total Records: ', total)
    print('Number of records predicted correctly = ', count)
    print('Accuracy = ', ((count / total)) * 100, '%')