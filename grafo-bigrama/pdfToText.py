#!/usr/bin/python3
import os
import sys
from tqdm import tqdm
import json

DIRETORIO_ATUAL = os.getcwd() 

def getArquivos(*args):
    arqList = list()
    for item in args:
        for p, _, files in os.walk(os.path.abspath(item)):
            for file in files:
                vel = os.path.join(p, file)
                arqList.append(vel)
    arqList.sort()
    return arqList

def getTextFromPdf( caminho:str ) -> str:
    os.popen(f"pdftotext \"{caminho}\"")

def getTextFromText( caminho:str) ->str:
    arq = open(caminho,"rb")
    string = arq.read().decode("utf8", errors="ignore")
    arq.close()
    return string

def salvaString( saida:str, string:str, caminho:str, primeiro:bool, var:dict ) ->None:
    var[ caminho.lstrip( DIRETORIO_ATUAL ) ] = string 

def inicioSaida(saida:str)->dict:
    return dict()
def fimSaida(saida:str, var:dict)->None:
    objJson = json.dumps(var,indent=2)
    arq = open( saida, "w")
    arq.write( objJson )
    arq.close()

def inicio(caminho:str, saida:str )->None:
    flag = True
    var = inicioSaida( saida )
    _caminhos = getArquivos( caminho )
    for caminho in tqdm( _caminhos ):
        if caminho.lower().endswith(".pdf"):
            getTextFromPdf( caminho )
    for caminho in tqdm( _caminhos ):        
        if caminho.lower().endswith(".txt"):
            string = getTextFromText( caminho )
            salvaString( saida , string, caminho , flag , var )
            flag = False
    fimSaida( saida , var )

if __name__ == "__main__":
    inicio( sys.argv[1], sys.argv[2])