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

indice = {}
my_re = re.compile('\W+')

def procesar_doc(doc):
    
    #Guardo como string el contenido del documento
    fitx = doc.read()
    #Deja las etiquetas en lineas separadas
    fitx = parser.parse(fitx)
    #Busqueda de los cuerpos de las noticias
    textos = parser.busqueda('TEXT',fitx)
    
    return textos

def indexar(parsed_doc, docid):
    #Para cada noticia en el documento
    for i in range(len(parsed_doc)):
        aux = parsed_doc[i]
        #Paso el texto a minuscula
        aux = aux.lower()
        #Elimino caracteres alfanumericos
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
    #Recorro los ficheros y creo el id del documento
    for fitxer in fitxers:
        doc = open(ruta+'/'+fitxer, 'r')
        pars_doc = procesar_doc(doc)
        docid = docid+1
        indexar(pars_doc,docid)
    
    pickle.dump(indice, open(index,'wb'))
