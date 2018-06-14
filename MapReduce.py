from collections import Counter
import requests, re
from time import time


class Reducer(object):
    _async = []
    _ref = []
    _ask = []
    _tell = ['start', 'receive_counting_words', 'receive_word_count', 'print_result']

    def start(self, N):
        self.timer = time()
        self.num_calls = 0
        self.dict = {}
        self.num_words = 0
        self.N = N

    def receive_word_count(self, dictionary):
        print "\nWord Count"
        print "RECIBIDO "
        self.dict = Counter(self.dict) + Counter(dictionary)
        self.num_calls = self.num_calls + 1
        if self.num_calls == self.N:
            self.print_result(self.dict)

    def receive_counting_words(self, count):
        print "\nCounting words"
        print "RECIBIDO " + str(count)
        self.num_words += count
        self.num_calls = self.num_calls + 1
        if self.num_calls == self.N:
            self.print_result(self.num_words)

    def print_result(self, result):
        print "\nRESULT: " + str(result)
        print "TIME: " + str(time() - self.timer)


class Mapper(object):
    _async = []
    _ref = ['start', 'counting_words']
    _ask = []
    _tell = ['start', 'word_count', 'counting_words']

    # Inicializar, coger la lineas que se procesaran y segun la variable: es_word_count hacer una cosa o la otra.
    def start(self, start, end, nom_fitxer, es_word_count, reducer):
        self.reducer = reducer
        text = requests.get("http://0.0.0.0:8000/%s" % nom_fitxer).text
        text = re.sub("[*1234567890',.;:_\[\]{}\-]", " ", text)
        text = re.sub('[" "]+ ', " ", text)
        text = text.lower()
        total_lines = text.split('\n')

        for i in range(len(total_lines)):
            total_lines[i] = total_lines[i].encode('latin1')

        lines = []

        for i in range(start, end):
            lines.append(total_lines[i])

        if es_word_count:
            self.word_count(lines)
        else:
            self.counting_words(lines)

    # Contar paraules diferents (diccionari)
    def word_count(self, lines):
        dict = {}
        for line in lines:
            for word in line.split(" "):
                if word != "":
                    if word in dict:
                        dict[word] = dict[word] + 1
                    else:
                        dict[word] = 1
        self.reducer.receive_word_count(dict)

    # Contar paraules (numero)
    def counting_words(self, text):
        count = 0

        for word in text:
            if word != "":
                count += len(word.split(" "))
        self.reducer.receive_counting_words(count)
