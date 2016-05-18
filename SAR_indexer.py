"""
    SAR indexer 
    Team: David Picornell Carpi
          Jose Miguel Benitez
"""
import sys
import re
import os
import pickle
import sgml_parser as parser

#Indices y lista que contendra los indices al guardarlos en disco
normalIndex = {}
titleIndex = {}
categoryIndex = {}
dateIndex = {}
finalIndex = []

my_re = re.compile('\W+')

def procesar_doc(doc, eti):
    
    #Guardo como string el contenido del documento
    fitx = doc.read()
    #Deja las etiquetas en lineas separadas
    fitx = parser.parse(fitx)
    #Busqueda de los cuerpos de las noticias
    textos = parser.busqueda(eti,fitx)
    
    return textos

def indexar(parsed_doc, docid,indice):
    #Para cada noticia en el documento
    for i in range(len(parsed_doc)):
        aux = parsed_doc[i]
        #Paso el texto a minuscula
        aux = aux.lower()
        #Elimino caracteres no alfanumericos
        aux = my_re.sub(' ',aux)
        #Transformamos en una lista de terminos
        aux = aux.split()
        posid = i
        #Creo el id final -> (id documento, posicion)
        finalid = (docid,posid)
        #Añado al indice        
        for j in range(len(aux)):
            term = aux[j]            
            if term not in indice:
                indice[term] = [finalid]

            elif finalid not in indice[term]:
                indice[term].append(finalid)
    
    return indice


if __name__ == '__main__':
    if(len(sys.argv)!=3):
        print('Usage: python3 SAR_indexer.py <ruta directorio> <nombre de indice>')
        sys.exit()

    ruta = sys.argv[1]
    index = sys.argv[2]
    fitxers = os.listdir(ruta)
    docid = 0
    #Recorro los ficheros buscando en los cuerpos de las noticias e indexando en su correspondiente indice
    for fitxer in fitxers:
        doc = open(ruta+'/'+fitxer, 'r')
        text_doc = procesar_doc(doc, 'TEXT')
        docid = docid+1
        indexar(text_doc,docid,normalIndex)

    #Recorro los ficheros buscando en los titulos e indexando en su correspondiente indice
    docid = 0
    for fitxer in fitxers:
        doc = open(ruta + '/' + fitxer, 'r')
        title_doc = procesar_doc(doc, 'TITLE')
        docid = docid + 1
        indexar(title_doc, docid, titleIndex)

    #Recorro los ficheros buscando en la etiqueta de categoria e indexando en su correspondiente indice
    docid = 0
    for fitxer in fitxers:
        doc = open(ruta + '/' + fitxer, 'r')
        cat_doc = procesar_doc(doc, 'CATEGORY')
        docid = docid + 1
        indexar(cat_doc, docid, categoryIndex)

    #Añado a una lista final todos los indices para guardarlos en disco
    finalIndex.append(normalIndex)
    finalIndex.append(titleIndex)
    finalIndex.append(categoryIndex)

    #Guardo el archivo en disco con el nombre que se le ha proporcionado por consola
    pickle.dump(finalIndex, open(index,'wb'))
