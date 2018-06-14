from pyactor.context import set_context, create_host, sleep, serve_forever
import os
import requests


# Se registran los nodos del sistema map_reduce
class Registry(object):
    _async = []
    _ref = ['bind', 'get_actors']
    _ask = ['get_num_actors', 'get_actors']
    _tell = ['bind']

    def __init__(self):
        self.actors = {}
        self.num_actors = 0

    def bind(self, actor):
        name = "actor%s" % self.num_actors
        self.actors[name] = actor
        self.num_actors += 1

    def get_actors(self):
        return self.actors.values()

    def get_num_actors(self):
        return self.num_actors


# Crear los slaves
def wake_up_slaves(N):
    port = 1238
    for i in range(N):
        port += 1
        command = "python Slave.py %s &" % port
        os.system(command)


# Se encarga de repartir las lineas entre los slaves
def split_file(num_mappers):
    text = requests.get("http://0.0.0.0:8000/%s" % nom_fitxer).text
    lines = text.split("\n")
    # print "NUM LINES: " + str(len(lines))

    buffer = len(lines) / num_mappers
    extra_buffer = len(lines) % num_mappers
    list = []
    for i in range(num_mappers):
        list.append(buffer)
    i = 0
    while extra_buffer > 0:
        list[i] += 1
        i = i + 1
        extra_buffer = extra_buffer - 1
    for i in range(1, num_mappers):
        list[i] += list[i - 1]

    return list


if __name__ == "__main__":
    set_context()
    master = create_host('http://127.0.0.1:1679')

    # Para
    # metros de entrada
    N = 2
    nom_fitxer = "200MB.txt"
    word_count = False

    os.system("python -m SimpleHTTPServer 8000 &")  # Crear un servidor con el fichero

    registry = master.spawn('registry', Registry)

    wake_up_slaves(N)

    print "Wait actors"
    while registry.get_num_actors() < N:
        sleep(0.2)
    actors = registry.get_actors()
    # print requests.get("http://0.0.0.0:8000/%s" % nom_fitxer).text  # Printear el texto
    list = split_file(N - 1)

    # Reducer
    reducer = actors[0].spawn("reducer", 'MapReduce/Reducer')  # El actor n 0 sera el reducer
    reducer.start(N - 1)  # Quitamos el reducer del total

    # Mappers
    for i in range(1, N):
        mapper = actors[i].spawn("mapper%s" % i, 'MapReduce/Mapper')
        if i == 1:
            mapper.start(0, list[i - 1], nom_fitxer, word_count, reducer)
        else:
            mapper.start(list[i - 2], list[i - 1], nom_fitxer, word_count, reducer)

    i = 0

    serve_forever()
