import leitorArquivo
import lendoArquivo
import gerando

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

    
if __name__ == "__main__":
    print("Gerando dados...")
    dados = gerandoDados()
    print("Montando grafo...")
    relacoes, autores = gerando.montandoGrafo( dados )
    print("Gerando grafo...")
    gerando.grafoGDF(relacoes, autores)
    print("Gerando tabela...")
    gerando.tabelaDeMaisCitado( relacoes, autores )