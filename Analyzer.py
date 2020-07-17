#!/usr/bin/env python3
from Graph import Node
from Graph import Edge
from Graph import Graph

from random import random
import jsonpickle
import sys

class Cluster():
	def __init__(self, nodes):
		self.roots = [n for n in nodes if n not in [e.end for e in n.inE]]
		self.nodes = nodes
		self.edges = [e for n in nodes for e in n.outE]
		self.in_edges = [e for n in self.nodes for e in n.inE if e.end not in self.nodes]
		self.out_edges = [e for n in self.nodes for e in n.outE if e.end not in self.nodes]
		assert self.Verify(), "The given nodes is not a connected graph"
		self.alloc = sum([n.size for n in nodes])
		self.reduce = sum([int(e.reload * e.begin.size) for e in self.edges])

	def Verify(self):
		all_nodes = self.nodes
		while len(all_nodes) > 1:
			n = all_nodes[0]
			valid = False
			for e in n.outE:
				if e.end in all_nodes:
					all_nodes.remove(e.end)
					valid = True
			all_nodes.remove(n)
			print(all_nodes)
			if not valid:
				return False
		return True

	def __repr__(self):
		return "Nodes: {}, Occupy: {:10,}, Reduce: {:10,}".format(
			[n.idx for n in self.nodes], self.alloc, self.reduce)

class Analyzer():
	def __init__(self, graph):
		self.g = graph
		self.next = [Cluster([x]) for x in self.g.GetNodes()]
		self.clusters = self.next
	def Run(self):
		while self.next:
			x = self.next.pop()
			print(x)
				

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("given a number of buffer size")
		exit(1)
	num = int(sys.argv[1])
	with open("rand.graph", 'r') as outf:
		frozen = outf.read()
	graph = jsonpickle.decode(frozen)
	print(graph)
	ana = Analyzer(graph)
	ana.Run()
