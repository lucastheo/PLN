#!/bin/usr/python3
import re

DATA_PADRAO = "\t"
CORTE_NOMES ="|"

def limpandoNome( string:str ):
    string = string.replace(".","")
    string = string.replace("'","")
    string = string.replace("_", " ")
    string = string.replace(","," ")
    string = string.strip(" ")
    string = re.sub(r"[ ]{2,}", " ",string )
    return string

def separandoNomes( string:str):
    if CORTE_NOMES in  string:
        var = list()
        for ele in string.split(CORTE_NOMES):
            var.append( ele.strip(" "))
        return var
    return[ string ]
    

def primeirasLetras(string:str, lista1:list ) -> list:
    if " " in string:
        lista = string.split(" ")
        for var in lista:
            if var != "":
                lista1.append(var[0])
        return lista1
        
    else:
        return lista1

def nomesList(string:str):
    if " " in string:
        return set( re.split("[ ]{1,}",string) )
    return set ( [ string ] )

class NomeAutor:
    def __init__(self, string):
        string = limpandoNome( string )
        self.string = string
        self.nomeLimpo = limpandoNome( self.string )
        self.primeirasLetras = primeirasLetras( self.nomeLimpo , list())
        self.nomesList = nomesList( self.nomeLimpo )
        
    def __eq__( self, other ):
        if self.nomeLimpo == other.nomeLimpo:
            return True

        if len( self.nomesList ) > 0 and len( other.nomesList )> 0:
            cont = 0
            for nome in self.nomesList:
                if len( nome ) > 1:
                    if nome in other.nomesList:
                        cont += 1
            if cont  > 1:
                return True
            if cont > 0:
                # temos um nome iguaç
                cont1 = 0
                
                for char in self.primeirasLetras:          
                    if char in other.primeirasLetras:
                        cont1 += 1
        
                if cont1 > 1: 
                    return True
        
        return False   
    def __hash__(self ):
        cont = 0
        controle = ord('g')
        for i in self.string:
            cont = ord( i ) - controle
        return cont
    def __str__(self):
        return self.nomeLimpo.title()

    def merge( self , other ):
        if len( self.string ) < len( other.string ):
            self.string = other.string
            
            self.nomeLimpo = limpandoNome( self.string )
        
        self.primeirasLetras = primeirasLetras( other.nomeLimpo, self.primeirasLetras )
        for i in nomesList( other.nomeLimpo ):
            if i != "":
                self.nomesList.add( i )
        

        
def retornaIndiceDaLista( lista, objCom ) -> int:
    for i , obj in enumerate( lista ):
        if obj == objCom:
            return i
    return -1

def pegandoAutoresPorArquivo(arquivo:str)->list:
    autoresLista = list()
    for linha in arquivo.splitlines():
        if linha != None:
            linha = linha.lower()
            for autores in separandoNomes( linha ):
                objNomeAutor = NomeAutor( autores )
                i = retornaIndiceDaLista( autoresLista , objNomeAutor  )

                if i != -1:
                    autoresLista[ i ].merge( objNomeAutor )
                else:
                    autoresLista.append( objNomeAutor )
    return autoresLista

if __name__ == "__main__":

    

    y = NomeAutor("Introna L") 
    x = NomeAutor("Introna Lucas")   

    print( x == y)