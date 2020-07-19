#!/usr/bin/env python3
from Graph import Node
from Graph import Edge
from Graph import Graph

from random import random
import jsonpickle
from graphviz import Digraph
import sys
sys.setrecursionlimit(9000000)

class Visualizer():
	def __init__(self, graph_name):
		with open(graph_name, 'r') as outf:
			frozen = outf.read()
		self.g = jsonpickle.decode(frozen)
		self.name = graph_name
	def Gen(self):
		G = Digraph('G', format='png', filename="{}".format(self.name))
		for n in self.g.nodes:
			half_mb = int(n.size * 2 / (1024 * 1024))
			if half_mb < 9:
				color = "/greys9/{}".format(half_mb+1)
			else:
				color = "/greys9/9"
			if half_mb < 6:
			    fontcolor = 'black'
			else:
			    fontcolor = 'white'
			G.node(str(n.idx),
				   "<{}>\ns:{:,}".format(n.idx, n.size),
				   fillcolor=color, style='filled', fontcolor=fontcolor)
		for e in self.g.edges:
			if (e.reload * 2) < 9:
				color = '/rdylgn9/{}'.format(9 - int(e.reload * 2))
			else:
				color = '/rdylgn9/9'
			G.edge(str(e.begin.idx), str(e.end.idx),
				   weight=str(e.reload),
				   label="{:4.3f}".format(e.reload),
				   width=str(e.reload),
				   arrowType='normal',
				   color=color)
		G.render()
		pass

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("given the graph name, default will read rand.graph")
		graph_name = "rand.graph"
	else:
		graph_name = sys.argv[1]
	viz = Visualizer(graph_name)
	viz.Gen()
