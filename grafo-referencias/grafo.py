import graphviz

def init():
    return graphviz.Digraph("grafo", filename= "grafo.png",engine="fdp")
def addNode( objGr:graphviz.Digraph, string:str):
    objGr.node(string)
def addVertice(objGr:graphviz.Digraph,string1:str,string2:str,cont):
    objGr.edge(string1,string2,attrs=cont)