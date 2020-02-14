import os 
import sys

def getArquivos(*args):
    arqList = list()
    for item in args:
        for p, _, files in os.walk(os.path.abspath(item)):
            for file in files:
                vel = os.path.join(p, file)
                arqList.append(vel)
    arqList.sort()
    return arqList

def get():
    var = dict()
    for caminho in getArquivos( "./dados" ):
        arq = open(caminho,"r")
        arqStr = arq.read()
        arq.close()
        chave = caminho.lstrip( os.getcwd())
        var[chave] = arqStr
    return var


