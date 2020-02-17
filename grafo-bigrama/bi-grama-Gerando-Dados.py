#!/usr/bin/python3

import json
import sys

def carregandoArquivo( caminho: str )->json:
    arq = open( caminho, "r")
    objJson = json.load( arq.read() )
    arq.close()

    return objJson

def 

if __name__ == "__main__":
    # este programa tem como objetivo pegar um json no formato "chave1":"chave2":inteiro e ordenar na forma "chave1 chave2":soma( inteiro )
    entrada = sys.argv[ 1 ]
    saida = sys.argv[ 2 ]