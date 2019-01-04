import operator
import time
import re
import numpy

headings = ['science', 'style', 'culture', 'life', 'economics', 'business', 'travel', 'forces', 'media', 'sport']
k = len(headings)
start = time.clock()
train_file =  open('news_data/news_train.txt', 'r', encoding='utf-8')
test_file =  open('news_data/news_test.txt', 'r', encoding='utf-8')
#print(train_file.readlines()[1].split('\t')[2].split(' '))
test_file = test_file.readlines()
train_file = train_file.readlines()
print(len(train_file))
print(len(test_file))

dictionary = {}
print(time.ctime(time.time()))
for line in train_file:
    line = re.sub(r'[!\.\?,):\-(»«\n]', ' ', line)
    # line.replace('.', ' ').replace('\n', ' ').replace(',', ' ').replace('(', ' ',).replace(')', ' ').replace('"', ' ').replace('«', ' ').replace('»', ' ').replace('!', ' ').replace('?', ' ').replace(':', ' ')
    line = line.lower().split('\t')
    head = line[0]
    tmp_dict = {}
    lines = line[1].split(' ')
    lines.extend(line[2].split(' '))
    # print(lines)
    for words in lines:
        if len(words) > 2:
            # print(words)
            i = tmp_dict.get(words)
            if i == None:
                tmp_dict.update({words: 1})
            else:
                tmp_dict.update({words: i + 1})
    j = dictionary.get(head)
    if j != None:
        for word in tmp_dict:
            if j.get(word) != None:
                j.update({word: j.get(word) + tmp_dict.get(word)})
            else:
                j.update({word: tmp_dict.get(word)})
        dictionary.update({head: j})
    else:
        dictionary.update({head: tmp_dict})


dicts = []
for head in headings:
    tmp_dict = dictionary.get(head)
    dict_sorted = sorted(tmp_dict.items(), key=operator.itemgetter(1), reverse=True)
    sorted_dict = []
    for i in range(0, len(dict_sorted)):
        v = dict_sorted[i][1]
        z = dict_sorted[int(len(dict_sorted) * 0.1)][1]
        if v > z:
            sorted_dict.append(dict_sorted[i])
    print(head, len(sorted_dict))
    dicts.append(sorted_dict)


all = 0
output_file = open('output.txt', 'w', encoding='utf-8')
start = time.clock()
for line in test_file:
    line = re.sub(r'[!\.\?,):\-(»«\n]', ' ', line)
    line = line.lower().split('\t')
    lines = line[0].split(' ')
    lines.extend(line[1].split(' '))
    predicts = []
    for heads in dicts:
        liness = numpy.array(lines)
        heads = numpy.array(heads)[:,0]
        predict = len(numpy.intersect1d(heads, lines))
        predicts.append(predict)
    predicts = numpy.array(predicts)

    output_file.write(headings[numpy.where(predicts == max(predicts))[0][0]]+'\n')

    #print(headings[numpy.where(predicts == max(predicts))[0][0]], predicts, max(predicts), line[0])
    #all+=1
    #print(all)


output_file.close()
