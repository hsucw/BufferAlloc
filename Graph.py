#!/usr/bin/env python3
import random

MAX_SIZE = 1024 * 1024 # 1MB
MIN_RELOAD = 0.8
MAX_RELOAD = 5.0

class Node():
	idx = 0
	def __init__(self):
		self.idx = Node.idx
		self.inE = []
		self.outE = []
		self.size = int(random.random() * MAX_SIZE)
		Node.idx += 1
	def AddInE(self, e):
		self.inE.append(e)
	def AddOutE(self, e):
		self.outE.append(e)
	def __repr__(self):
		return "Node: <{}>, size: {:10,}, in:{}, out:{}".format(
				self.idx, self.size, [x.idx for x in self.inE], [x.idx for x in self.outE])

class Edge():
	idx = 0
	def __init__(self, B, E):
		self.idx = Edge.idx
		self.begin = B
		self.end = E
		self.reload = random.uniform(MIN_RELOAD, MAX_RELOAD)
		B.AddOutE(self)
		E.AddInE(self)
		Edge.idx += 1
	def GetSize(self, size):
		return self.size
	def GetReload(self, size):
		return self.reload * self.size
	def __repr__(self):
		return "Edge: <{}>, {} -> {}, reload: {:.2f} X".format(
				self.idx, self.begin.idx, self.end.idx, self.reload)

class Graph():
	def __init__(self):
		self.root = None
		self.nodes = []
		self.edges = []
	def CreateNode(self):
		n = Node()
		self.nodes.append(n)
		return n
	def CreateEdge(self, B, E):
		assert B.idx is not E.idx, "Cannot self connected " + str(B) + ", " + str(E)
		for mEdge in self.edges:
			if mEdge.begin.idx is B.idx and mEdge.end.idx is E.idx:
				return mEdge
		e = Edge(B, E)
		self.edges.append(e)
		return e
	def GetNodes(self):
		return self.nodes.copy()
	def GetNode(self, idx):
		for n in self.nodes:
			if idx == n.idx:
				return n
		return None
	def GetEdges(self):
		return self.edges.copy()
	def GetEdge(self, idx):
		for n in self.edges:
			if idx == n.idx:
				return n
		return None
	def Verify(self):
		for n in self.nodes:
			cnt = 0
			for x in self.nodes:
				if n.idx is x.idx:
					cnt += 1
			assert cnt is 1
		for e in self.edges:
			cnt = 0
			for y in self.edges:
				if e.idx is y.idx:
					cnt += 1
			assert cnt is 1
	def __repr__(self):
		out = ""
		out += "== Graph ==\n"
		for n in self.nodes:
			out += "{}\n".format(n)
		for e in self.edges:
			out += "{}\n".format(e)
		out += "-----------\n"
		return out


if __name__ == "__main__":
	g = Graph()
	x = g.CreateNode()
	y = g.CreateNode()
	e = g.CreateEdge(x, y)
	print(g)
	x = g.CreateNode()
	e = g.CreateEdge(x, y)
	print(g)
	y = g.CreateNode()
	x = g.CreateNode()
	e = g.CreateEdge(x, y)
	

	n = Node()
	x = Node()
	print(n)
	print(x)
	e = Edge(n, x)
	print(e)
	e = Edge(x, n)
	print(e)
	print(n)
	print(x)

