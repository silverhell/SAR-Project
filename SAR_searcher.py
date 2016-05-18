"""
    SAR searcher
    Team: David Picornell Carpi
          Jose Miguel Benítez
"""
import sys

if __name__ == '__main__':
    if(len(sys.argv)!= 2):
        print("Usage: python3 SAR_searcher.py <index> optional parameters: <stopwords> <stemming>")
        sys.exit()
    while True:
        consulta = input('Introduce tu consulta:\n')
        if consulta == '':
            print('Hasta la proxima')
            sys.exit()