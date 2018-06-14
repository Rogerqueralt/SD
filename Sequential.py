import requests, re
from time import time


# contar paraules diferents
#revisar!!!!!!
def word_count(data):
    dict = {}
    for line in data:
        for word in line.split(" "):
            if word != "":
                if word in dict:
                    dict[word] = dict[word] + 1
                else:
                    dict[word] = 1

    return dict


# contar paraules
def counting_words(data):
    count = 0
    for word in data:
        if word != "":
            count += len(word.split(" "))

    return count


if __name__ == "__main__":

    fitxer = '800MB.txt'

    #duplicar la opertura i tractament de text i el tancament
    temps1 = time()
    abierto = open(fitxer)
    text = abierto.read()
    text = re.sub("[*1234567890',.;:_\[\]{}\-]", " ", text)
    text = re.sub('[" "]+ ', " ", text)
    text = text.lower()
    text = text.split('\n')

    print 'counting words'

    num_paraules = counting_words(text)
    abierto.close()
    print "total paraules:"
    print num_paraules
    print "time counting words: " + str(time() - temps1)

    temps2 = time()
    abierto2 = open(fitxer)
    text = abierto2.read()
    text = re.sub("[*1234567890',.;:_\[\]{}\-]", " ", text)
    text = re.sub('[" "]+ ', " ", text)
    text = text.lower()
    text = text.split('\n')
    print " "
    print 'word count'

    dict = word_count(text)
    abierto2.close()
    #print dict
    print "time word count: " + str(time() - temps2)

