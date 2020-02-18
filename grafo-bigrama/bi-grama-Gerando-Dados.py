#!/usr/bin/python3

import json
import sys
import graphviz

def carregandoArquivo( caminho: str )->json:
    arq = open( caminho, "rb")
    objJson = json.load( arq )
    arq.close()

    return objJson

def foramantandoDadoPelaPastaRaiz( var:json ):
    #percorre o nome dos arquivos

    apo1 = dict()           # contagem em todos
    apo2 = dict()           # contagem sumarizado

    for nomeArq in var:
        reducaoNomeArq = pegandoPastaRaiz( nomeArq )
        if reducaoNomeArq not in apo1.keys():
            apo1[ reducaoNomeArq ] = dict()
    
    # temos uma dict(nome_dos_arquivos_reduzidos)  precisamos add as relacoes das palavras
    for nomeArq in var:
        reducaoNomeArq = pegandoPastaRaiz( nomeArq )
        
        for palavra1 in var[ nomeArq ]: 

            if len( palavra1 ) > 2:
                for palavra2 in var[ nomeArq ][ palavra1 ]:
                    
                    if len( palavra2  ) > 2:
                        soma = palavra1 + " " + palavra2

                        if soma not in apo1[ reducaoNomeArq ]:
                            apo1[ reducaoNomeArq ][ soma ] = var[ nomeArq ][ palavra1 ][ palavra2 ]
                        else:
                            apo1[ reducaoNomeArq ][ soma ] += var[ nomeArq ][ palavra1 ][ palavra2 ]
                        
                        if soma not in apo2:
                            apo2[ soma ] = var[ nomeArq ][ palavra1 ][ palavra2 ]
                        else:
                            apo2[ soma ] += var[ nomeArq ][ palavra1 ][ palavra2 ]
                    
    return apo1, apo2

def formatandoSaidaTSV( saida:str , var:dict ):
    s = "Palavras\tContagem\n"
    for chave in sorted( var , key=var.__getitem__ ,reverse=True ):
        s += f"{chave}\t{var[ chave ]}\n"
    
    arq = open( saida, "w")
    arq.write( s )
    arq.close()

def geraSaidaTSV( saidaBase:str, classificado:dict, sumarizado:dict):
    for chave in classificado.keys():
        formatandoSaidaTSV(  f"{saidaBase}{chave}.tsv" ,classificado[ chave ] )
    formatandoSaidaTSV(  f"{saidaBase}todos.tsv" , sumarizado )

def verificaNode( objGrafo, apoSet:set ,palavra:str ):
    if palavra not in apoSet:
        apoSet.add( palavra )
        objGrafo.node( palavra )
def addAresta( objGrafo, palavra1:str, palavra2:str, peso:int):
    objGrafo.edge( palavra1, palavra2, str( peso ) )
    

def formataSaidaGrafo( saida:str, var:dict ):
    apoSet = set()
    objGrafo = graphviz.Graph(   )
    objGrafo.attr(label = saida.replace("./dados/conjunto/", "").replace("_", " ") )

    for chave in sorted( var , key=var.__getitem__ ,reverse=True ):
        if len( apoSet ) > 20:
            break
        
        palavras = chave.split(" ")
        verificaNode( objGrafo, apoSet , palavras[ 0 ])
        verificaNode( objGrafo, apoSet,  palavras[ 1 ])
    
        addAresta( objGrafo , palavras[ 0 ], palavras[ 1 ] , var[ chave ])

    objGrafo.engine = "dot"

    objGrafo.render( saida  ,format= "png"  )

def geraSaidaGrafo( saidaBase:str, classificado:dict, sumarizado:dict ):
    for chave in classificado.keys():
        formataSaidaGrafo( f"{saidaBase}{chave}", classificado[ chave])
    formataSaidaGrafo( f"{saidaBase}todos", sumarizado )

def pegandoPastaRaiz( string:str )->str:
    if "/" not in string:
        return string

    if string.endswith("/"):
        string = string.rstrip("/")
    
    apo = string.split("/")

    if len( string ) > 1:
        return apo[ -2 ]
    elif len( apo ) == 1:
        return apo[ 0 ]
    
    return string
    


if __name__ == "__main__":
    # este programa tem como objetivo pegar um json no formato "arquivo":"chave1":"chave2":inteiro e ordenar na forma "pastaInicio""chave1 chave2":soma( inteiro )
    
    entrada = sys.argv[ 1 ]
    saida = sys.argv[ 2 ]

    dados = carregandoArquivo( entrada )
    classificado, sumarizado = foramantandoDadoPelaPastaRaiz( dados )
    geraSaidaTSV( saida, classificado, sumarizado )
    geraSaidaGrafo( saida, classificado, sumarizado)

 