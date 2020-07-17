#!/usr/bin/env python3
from Graph import Node
from Graph import Edge
from Graph import Graph

from random import random
import jsonpickle
import sys
sys.setrecursionlimit(9000000)

class Builder():
	def __init__(self):
		self.g = Graph()
	def GetGraph(self):
		return self.g
	def PickRandomNode(self):
		nodes =  self.g.GetNodes()
		node_size = len(nodes)
		if node_size is 0:
			return None
		i = int(random() * node_size)
		return nodes[i]
	def PickRandomNodePair(self):
		nodes = self.g.GetNodes()
		node_size = len(nodes)
		if len(nodes) < 2:
			return (None, None)
		i = int(random() * node_size)
		j = i
		while j == i:
			j = int(random() * node_size)
		assert i is not j, "cannot pick a pair of a same node"
		return (nodes[min(i, j)], nodes[max(i,j)])
		
	def CreateRandomNode(self):
		x = self.PickRandomNode()
		y = self.g.CreateNode()
		if x is not None:
			assert x.idx is not y.idx
			e = self.g.CreateEdge(x, y)
		return y

	def CreateRandomEdge(self):
		x, y = builder.PickRandomNodePair()
		if x is None or y is None:
			self.CreateRandomNode()
			return None
		else:
			assert x.idx is not y.idx
			e = builder.g.CreateEdge(x, y)
			return e
	

if __name__ == "__main__":
	builder = Builder()
	if len(sys.argv) < 2:
		print("given a number of random object (nodes, edges)")
		exit(1)
	num = int(sys.argv[1])
	for x in range(num):
		# 80% create edges
		addEdge = (random() > 0.2)
		if addEdge:
			builder.CreateRandomEdge()
		else: 
			builder.CreateRandomNode()
	frozen = jsonpickle.encode(builder.GetGraph(), indent=4, separators=(', ', ': '))
	with open("rand.graph", 'w') as outf:
		outf.write(frozen)
	print(builder.GetGraph())
