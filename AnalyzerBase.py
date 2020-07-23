#!/usr/bin/env python3
from Graph import Node
from Graph import Edge
from Graph import Graph

from random import random
import pydotplus
import sys
import jsonpickle
sys.setrecursionlimit(9000000)

class AnalyzerBase():
    def __init__(self, graph_name):
        G = pydotplus.graphviz.graph_from_dot_file(graph_name)
        self.g = Graph()
        node_num = len(G.get_nodes())
        edge_num = len(G.get_edges())
        nodes = [None] * node_num
        edges = [None] * edge_num
        for i in range(node_num):
            nodes[i] = self.g.CreateNode()
        for n in G.get_nodes():
            size = int(n.get_label().split()[1].split(':')[1].replace(',','').replace('"',''))
            nodes[int(n.get_name())].SetSize(size)
        for i in range(edge_num):
            e = G.get_edges()[i]
            src = int(e.get_source())
            dst = int(e.get_destination())
            weight = float(e.get_weight())
            edge = self.g.CreateEdge(nodes[src], nodes[dst])
            edge.SetReload(weight)
            assert edge.idx == i
        self.res={}
        self.analysis={}
        self.name="Base"
        #print(self.g)
    def Run(self):
        print("not yet implement")

    def SetName(self, name):
        self.name = name

    def GetName(self):
        return self.name

    def SaveRes(self):
        frozen = jsonpickle.encode(self.res, indent=4, separators=(', ', ': '))
        with open(self.name + ".json", 'w') as outf:
            outf.write(frozen)

    def GetRes(self, name):
        with open(name + ".json", 'r') as outf:
            frozen = outf.read()
        self.analysis[name] = jsonpickle.decode(frozen)
