import leitorArquivo

def depuplicarLista( var0:list ) -> list:
    var1 = list()
    for obj0 in var0:
        if -1 == leitorArquivo.retornaIndiceDaLista( var1 , obj0 ):
            var1.append( obj0 )
    return var1

def montandoGrafo(var:dict ):
    autores = list()
    for autorChave in var.keys():
        if -1 == leitorArquivo.retornaIndiceDaLista( autores , autorChave ):
            autores.append( autorChave )
        for autorCitados in var[ autorChave ]:
            if -1 == leitorArquivo.retornaIndiceDaLista( autores , autorCitados ):
                autores.append( autorCitados )
    
    autores = depuplicarLista( autores )

    relacao = dict()
    for autorChave in var.keys():
        idAutorChave =  leitorArquivo.retornaIndiceDaLista( autores , autorChave )
        if idAutorChave not in relacao.keys():
            relacao[ idAutorChave ] = set() 
        
        for autorCitados in var[ autorChave ]:
            idAutorCitado = leitorArquivo.retornaIndiceDaLista( autores , autorCitados )
            relacao[ idAutorChave ].add( idAutorCitado )
    return relacao, autores
    
def grafoGDF(relacao:dict, autores:list ):

    s = "nodedef>name VARCHAR, label nome, chave BOOLEAN\n"
    for i , autor in enumerate( autores ):
        ehAutorChave  = i in relacao.keys()
        s += f"{i},{autor},{ehAutorChave}\n"

    s += "edgedef>node1 VARCHAR, node2 VARCHAR, directed BOOLEAN\n"
    for idAutorChave in relacao.keys():
        for idAutorCitado in relacao[ idAutorChave ]:
            s += f"{idAutorChave},{idAutorCitado}\n"

    arq = open("./grafo.gdf", "w")
    arq.write( s )
    arq.close()

    

    #-Contando-a-quantidade de-referencias
def tabelaDeMaisCitado( relacao:dict, autores:list ): 
    contagemDeCitacao = dict()
    for idAutorChave in relacao.keys():
        for idAutorCitado in relacao[ idAutorChave ]:
            if idAutorCitado not in contagemDeCitacao:
                contagemDeCitacao[ idAutorCitado  ] = 1
            else:
                contagemDeCitacao[ idAutorCitado ] += 1
    
    s = "Nome, Citado_quantas_vezes\n"

    for i in contagemDeCitacao:
        s += f"{autores[i]}\t{contagemDeCitacao[ i  ]}\n"

    arq = open("./contagem.tsv", "w")
    arq.write( s )
    arq.close()