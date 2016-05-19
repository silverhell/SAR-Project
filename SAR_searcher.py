"""
    SAR searcher
    Team: David Picornell Carpi
          Jose Miguel Benítez
"""
import sys
import pickle
import nltk
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import SAR_indexer as indexer

operadores = [AND, OR, NOT]

def algoritmoOR(tuples1,tuples2):
    res = indexer.algoritmoOR_int(tuples1,tuples2)
    return res

def algoritmoAND(tuples1, tuples2):
    i = 0
    j = 0
    res = []
    while(i<len(tuples1) and j<len(tuples2)):
        if tuples1[i] < tuples2[j]:
            i += 1
        elif tuples1[i] > tuples2[j]:
            j += 1
        else:
            res.append(tuples1[i])
            i += 1
            j += 1
    return res

def algoritmoNOT(tuples, stem):
    lengths = indices[6]
    lengths = list(lengths.values())
    res = []
    i = 1
    j = 1
    k = 0
    l = 0
    final = False
    while(j<=lengths[l]):
        tupla = (i, j)
        if tupla < tuples[k]:
            res.append(tupla)
            j += 1
        else:
            j += 1
            k += 1

        if j == lengths[l]:
            l += 1
            i += 1
            j = 1

    return res

def busquedaLiteral(busqueda, stem):
    if not stem:
        indice = indices[3]
    else:
        indice = indices[0]

    busqueda = busqueda.split()
    diccionaris = []
    for i in range(len(busqueda)):
        diccionaris.append(indice[busqueda[i]])

    tuples = diccionaris[0].keys()


def parseConsulta(consulta):
    

def snippets(noticia, busqueda):
    snippet = []
    busquedaSnippet = []

    for word in busqueda:
        if word not in operadores and not (':' in word):
            busquedaSnippet.append(word)
    noticia = noticia.split('.')
    for sentence in noticia:
        for paraula in busquedaSnippet:
            if sentence.find(paraula) >= 0:
                snippet.append(sentence)
                busquedaSnippet.remove(paraula)
    finalSnippet = '[...]'.join(sentence)
    return finalSnippet

def remove_stopwords(wordlist, idioma):
    stopwords = nltk.corpus.stopwords.words(idioma)
    result = [w for w in wordlist if w.lower() not in stopwords]
    return result

if __name__ == '__main__':
    if(len(sys.argv)!= 4):
        print("Usage: python3 SAR_searcher.py <index> optional parameters: <stopwords> <stemming>")
        print("Si no quieres activar los parametros opcionales, escribe 0")
        sys.exit()

    #Cargo el archivo binario con la lista de indices
    index = open(sys.argv[1],'rb')
    indices = pickle.load(index)

    #Bucle de consultas
    while True:
        consulta = input('Introduce tu consulta:\n')
        if consulta == '':
            print('Hasta la proxima')
            sys.exit()
        literal = False

        if consulta[0] == '\"' and consulta[len(consulta)-1] == '\"':
            literal = True




        if(sys.argv[2] != '0' and sys.argv[3] == '0' and not literal):
            #Quitar stopwords
            consulta = remove_stopwords(consulta.split(),'spanish')

        if(sys.argv[3] != '0' and sys.argv[2] == '0'):
            #Aplicar stemming
            stemmer = SnowballStemmer('spanish')
            consulta = consulta.split()
            for i in range(len(consulta)):
                if consulta[i] not in operadores:
                    consulta[i] = stemmer.stem(consulta[i])

        if(sys.argv[2] != '0' and sys.argv[3] != '0'):
            if not literal:
                consulta = remove_stopwords(consulta.split(), 'spanish')
            for i in range(len(consulta)):
                if consulta[i] not in operadores:
                    consulta[i] = stemmer.stem(consulta[i])

