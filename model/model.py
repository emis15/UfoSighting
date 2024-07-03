import copy

import networkx as nx
from database.DAO import DAO
from geopy import distance


class Model:
    def __init__(self):
        self.years = []
        self.graph = nx.Graph()
        self.bestPath = []
        self.bestSol = 0
        self.idMap = {}
        self.graph.add_nodes_from(DAO.getNodes())
        for s in self.graph.nodes:
            self.idMap[s.id] = s


    def buildGraph(self, year, shape):
        print(self.numNodes())
        self.graph.clear_edges()
        self.graph.add_weighted_edges_from(DAO.getAllWeightedNeigh(year, shape, self.idMap))
        #edges = DAO.getEdges(self.idMap)
        #for e in edges:
        #        weight = DAO.getWeight(year, shape, e)
        #        self.graph.add_edge(e[0], e[1], weight = weight)
        print(self.numEdges())

    def calcola_Percorso(self):
        self.bestPath = []
        self.bestSol = 0
        for n in self.graph.nodes:
            parziale = []
            parziale.append(n)
            self.ricorsione(parziale)


    def ricorsione(self, parziale):
        ammissibili = []
        ammissibili_tupla = []
        neigh = list(self.graph.neighbors(parziale[-1]))
        if len(parziale)<2:
            ammissibili = list(neigh)
        else:
            for n in neigh:
                if self.graph[parziale[-1]][n]['weight']>self.graph[parziale[-2]][parziale[-1]]['weight']:
                    ammissibili.append(n)
        if len(ammissibili) == 0:
            weight = 0
            for i in range (0, len(parziale)-1):
                weight += self.distanza(parziale[i],parziale[i+1])
            if weight > self.bestSol:
                self.bestSol = weight
                self.bestPath = copy.deepcopy(parziale)
            return
        for n in ammissibili:
            ammissibili_tupla.append((n, self.graph[parziale[-1]][n]['weight']))
        ammissibili_tupla.sort( key=lambda x: x[1])
        for n in ammissibili_tupla:
            parziale.append(n[0])
            self.ricorsione(parziale)
            parziale.pop()
        return


    def sommaArchi(self, n):
        peso = 0
        for e in self.graph.edges(n, data=True):
            peso += e[2]['weight']
        return peso

    def distanza(self, n1, n2):
        coords_1 = (n1.Lat, n1.Lng)
        coords_2 = (n2.Lat, n2.Lng)
        distance_geo = distance.geodesic(coords_1, coords_2).km
        return distance_geo
    def getYears(self):
        return DAO.getAllYears()

    def getShapes(self, year):
        return DAO.getShapesfromYear(year)
    def numNodes(self):
        return len(self.graph.nodes)
    def numEdges(self):
        return len(self.graph.edges)

    def build_graph_tema_passato(self, anno, giorni):
        self.graph.add_weighted_edges_from(DAO.getAllPesiTemaPassato(anno, giorni, self.idMap))