import leitorArquivo
import lendoArquivo
import grafo

def gerandoDados():
    arquivosDict = lendoArquivo.get()
            
    var = dict() # Armazena as relações das pessoas
    
    for chave in arquivosDict.keys():

        for autorChave in leitorArquivo.pegandoAutoresPorArquivo( chave ):
            if autorChave not in var.keys():
                var[ autorChave ] = list()
            for autorCitados in leitorArquivo.pegandoAutoresPorArquivo( arquivosDict[ chave ]):
                var[ autorChave ].append( autorCitados )
    return var

def gerandoGrafo(var:dict):
    #gerando Vertice
    
    objGr = grafo.init()
    for autorChave in var.keys():
        grafo.addNode( objGr, str( autorChave ) )
        for autorCitados in var[ autorChave ]:
            grafo.addNode( objGr, str( autorCitados ) )
    
    var1 = dict() #armazena as arestas do grafo ( retira redundancia )
    for autorChave in var.keys():
        if autorChave not in var1.keys():
            var1[ autorChave ] = set()
        for autorCitados in var[ autorChave ]:
            var1[ autorChave ].add( str( autorCitados) ) 
    
    for autorChave in var1.keys():
        for autorCitados in var1[ autorChave ]:
            grafo.addVertice( objGr, str( autorChave ), str( autorCitados ), "1")

    objGr.render("grafo.pdf",format="png")

def depuplicarLista( var0:list ) -> list:
    var1 = list()
    for obj0 in var0:
        if -1 == leitorArquivo.retornaIndiceDaLista( var1 , obj0 ):
            var1.append( obj0 )
    return var1

def gerandoGrafoGDF(var:dict):
    #gerando Vertice

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

    
if __name__ == "__main__":
    print("Gerando dados...")
    dados = gerandoDados()
    print("Gerando grafo...")
    gerandoGrafoGDF(dados)