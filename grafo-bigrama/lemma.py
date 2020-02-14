#!/usr/bin/python3
import json
from textblob import TextBlob
from textblob import WordList
import re
import sys
from tqdm import tqdm

REGEX_PALAVRAS = r"['a-zA-ZÀ-ÖØ-öø-ÿ0-9]+"

#carrega o arquivo
def loadFile( entrada:str ):
    arq = open( entrada , "rb")
    objJson = json.load( arq )
    arq.close()
    return objJson 

#percorre os vários arquivos, a estrutura eh basicamento um dict de uma lista1 com listas2 dentro. 
# Onde o dict.keys() é o caminho
# listas2 uma lista de palavras lematizadas
def percorreArquivos( var:json):
    estrutura = dict()
    for strArq in tqdm( var ):
        estrutura[ strArq ] = list()
        for conjunto in cortaPeloPonto( var[ strArq ] ):
            if len( conjunto ) > 0:

                conjunto = conjunto.lower()

                apo1 = pegaTodasAsPalavras( conjunto )
                apo2 = lematizacaoDaListaTexto( apo1 )
                estrutura[strArq].append( apo2 )
    return estrutura

def cortaPeloPonto( string:str)->list:
    if "." in string:
        return string.split(".")
    return [string]
#corta o arquivo em palavras
def pegaTodasAsPalavras( string:str )->list:    
    return re.findall(REGEX_PALAVRAS, string )

def lematizacaoDaListaTexto( var:list )->list:
    objWl = WordList( var  )
    return objWl.lemmatize()





####################################################

def carregaDict( var:dict, chave ):
    if chave not in var.keys():
        var[ chave ] = dict()
def somaMaisUm( var: dict , chave ):
    if chave not in var.keys():
        var[ chave ] = 1
    else:
        var[ chave ] += 1

def geraRelacaoEntrePalavras( var: dict, lista:list ):
    for i in range( 0 , len( lista ) ):
        palavra1 = lista[ i ]
        for j in range( i + 1 , len( lista ) ):
            palavra2 = lista[ j ]

            if palavra1 < palavra2:
                palavra1, palavra2 = palavra2, palavra1
            
            carregaDict( var , palavra1 )
            somaMaisUm( var[ palavra1 ], palavra2 )
            

            
            

def geraRelacioanmento( var:dict )->list:
    #nível arquivo
    resul = dict()
    for caminho in tqdm( var.keys() ):
        carregaDict( resul , caminho )

        # texto é uma lista de lista de palavras
        for texto in var[ caminho ]:
            geraRelacaoEntrePalavras( resul[ caminho ] , texto )
    return resul

def armazenaSaida( saida:str, var:dict )->None:
    objJson = json.dumps(var, indent=2)

    arq = open( saida, "w" )
    arq.write( objJson )
    arq.close()
        


if __name__ == "__main__":
    arq = loadFile( sys.argv[1] )
    # percorre os arquivos já aplicando a lematizacao
    fase1 = percorreArquivos( arq )

    #gera a contagem de relações das palavras como bigramas
    fase2 = geraRelacioanmento( fase1 )

    armazenaSaida( sys.argv[2] , fase2 )