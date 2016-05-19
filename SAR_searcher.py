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
import os


#Utils
operadores = ['AND', 'OR', 'NOT']
defaultOperator = 'AND'
etis = ['headline','category','text']


#ALGORITMO OR
def algoritmoOR(tuples1,tuples2):
    res = indexer.algoritmoOR_int(tuples1,tuples2)
    return res
#Fin algoritmoOR


#ALGORITMO AND
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
#Fin algoritmoAND


#EL MILLOR NOT DE TOTA LA PROMOCIO
def algoritmoNOT(tuples):
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
#Fin algoritmoNOT

def algoritmoANDNOT(tuples1, tuples2):
    res = []
    not_tuples2 = algoritmoNOT(tuples2)
    res = algoritmoAND(tuples1,not_tuples2)
    return res
#Fin algoritmoANDNOT


def algoritmoORNOT(tuples1, tuples2):
    res = []
    not_tuples2 = algoritmoNOT(tuples2)
    res = algoritmoOR(tuples1, not_tuples2)
    return res
    # Fin algoritmoORNOT


#TO BE IMPLEMENTED PERO QUE FLIPES
def busquedaLiteral(busqueda, stem):
    if not stem:
        indice = indices[0]
    else:
        indice = indices[3]

    busqueda = busqueda.split()
    diccionaris = []
    for i in range(len(busqueda)):
        diccionaris.append(indice[busqueda[i]])

    tuples = diccionaris[0].keys()
#Fin busquedaLiteral


def busquedaUnaParaula(paraula, index):
    diccionari = index[paraula]
    posting = list(diccionari.keys())
    return posting
#Fin busquedaUnaParaula


def consultaEtis(consulta,stem):
    res = []
    for i in range(len(consulta)):
        elem = consulta[i]
        if elem.find(':') > 0:
            consulta = consulta[i].split(':')

    for i in range(len(consulta)):
        word = consulta[i]
        if word in etis:
            if word == 'headline':
                if not stem:
                    indice = indices[1]
                    res = busquedaUnaParaula(consulta[i+1],indice)
                else:
                    indice = indices[4]
                    res = busquedaUnaParaula(consulta[i + 1], indice)
            elif word == 'category':
                if not stem:
                    indice = indices[2]
                    res = busquedaUnaParaula(consulta[i + 1], indice)
                else:
                    indice = indices[5]
                    res = busquedaUnaParaula(consulta[i + 1], indice)
            elif word == 'text':
                if not stem:
                    indice = indices[0]
                    res = busquedaUnaParaula(consulta[i + 1], indice)
                else:
                    indice = indices[3]
                    res = busquedaUnaParaula(consulta[i + 1], indice)
    return res
#Fin consultaEtis


#TO BE IMPLEMENTED
def parseConsulta(consulta,stem):
    if not stem:
        indice = indices[0]
    else:
        indice = indices[3]
    res = []

    for i in range(len(consulta)):
        word = consulta[i]
        if word in operadores and word != defaultOperator:
            if word == 'OR' and consulta[i+1]!='NOT':
                tuples1 = indice[consulta[i-1]]
                tuples2 = indice[consulta[i+1]]
                res = algoritmoOR(tuples1, tuples2)

            elif word == 'OR' and consulta[i+1]=='NOT':
                tuples1 = indice[consulta[i-1]]
                tuples2 = indice[consulta[i+2]]
                res = algoritmoORNOT(tuples1, tuples2)

            elif word == 'NOT':
                tuples = indice[consulta[i+1]]
                res = algoritmoNOT(tuples)

        elif word == defaultOperator and consulta[i+1] != 'NOT':
            tuples1 = indice[consulta[i-1]]
            tuples2 = indice[consulta[i+1]]
            res = algoritmoAND(tuples1, tuples2)

        elif word == defaultOperator and consulta[i+1] == 'NOT':
            tuples1 = indice[consulta[i - 1]]
            tuples2 = indice[consulta[i + 2]]
            res = algoritmoANDNOT(tuples1, tuples2)

    return res
#Fin parseConsulta


def snippets(noticia, busqueda):
    snippet = []
    busquedaSnippet = []

    #Busqueda de terminos que no sean operadores o etiquetas
    for word in busqueda:
        if word not in operadores and not (':' in word):
            busquedaSnippet.append(word)
    noticia = noticia.split('.')
    #Busqueda de oraciones donde aparezcan las palabras validas para crear el snippet
    for sentence in noticia:
        for paraula in busquedaSnippet:
            if sentence.find(paraula) >= 0:
                snippet.append(sentence)
                busquedaSnippet.remove(paraula)
    #Creo el conjunto de snippets separandolos con el separador que implica texto omitido
    finalSnippet = '[...]'.join(sentence)
    return finalSnippet
#Fin snippets


#TO BE IMPLEMENTED
def retorno(posting, busqueda):
    ficheros = os.listdir(index)

    if len(posting) <=2:
        #Print titulo y cuerpo de las noticias

        print('To do')
    elif len(posting) > 2 and len(posting) <=5:
        #Print titulo y snippets
        print('To do')
    else:
        #Print titulos
        print('To do')

    #En todos los casos, print del tamaño total
    print(len(posting))
#Fin retorno


#Metodo para eliminar stopwords de una lista de palabras
def remove_stopwords(wordlist, idioma):
    stopwords = nltk.corpus.stopwords.words(idioma)
    result = [w for w in wordlist if w.lower() not in stopwords]
    return result
#Fin remove_stopwords


#FALTA IMPLEMENTAR COSAS
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
        stem = False

        #Comprobacion de banderas
        if sys.argv[3] != '0':
            stem = True

        if consulta[0] == '\"' and consulta[len(consulta)-1] == '\"':
            literal = True

        #Ningun extra activado y consulta de una palabra o una etiqueta
        if (sys.argv[2] == '0' and sys.argv[3] == '0'):
            consulta = consulta.split()
            if len(consulta) == 1 and consulta[0].find(':')==-1:
                if not stem:
                    indice = indices[0]
                else:
                    indice = indices[3]
                res = busquedaUnaParaula(consulta[0], indice)
                print(len(res))
            else:
                res = consultaEtis(consulta,stem)
                print(len(res))

        #Activado solo stopwords
        if(sys.argv[2] != '0' and sys.argv[3] == '0' and not literal):
            #Quitar stopwords
            consulta = remove_stopwords(consulta.split(),'spanish')

        #Activado solo stemming
        if(sys.argv[3] != '0' and sys.argv[2] == '0'):
            #Aplicar stemming
            stemmer = SnowballStemmer('spanish')
            consulta = consulta.split()
            for i in range(len(consulta)):
                if consulta[i] not in operadores:
                    consulta[i] = stemmer.stem(consulta[i])

        #Activado tanto stopwords como stemming
        if(sys.argv[2] != '0' and sys.argv[3] != '0'):
            stemmer = SnowballStemmer('spanish')
            if not literal:
                consulta = remove_stopwords(consulta.split(), 'spanish')
            for i in range(len(consulta)):
                if consulta[i] not in operadores:
                    consulta[i] = stemmer.stem(consulta[i])



