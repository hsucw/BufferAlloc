#!/usr/bin/env python3
from AnalyzerBase import AnalyzerBase
import jsonpickle
import sys

def Cost(alloc, reload_size):
	return reload_size * 1.0 / (alloc)

class Cluster():
	def __init__(self, nodes):
		self.roots = [n for n in nodes if n not in [e.end for e in n.inE]]
		self.nodes = nodes
		self.edges = [e for n in nodes for e in n.outE]
		self.in_edges = [e for n in self.nodes for e in n.inE if e.begin not in self.nodes]
		self.out_edges = [e for n in self.nodes for e in n.outE if e.end not in self.nodes]
		assert self.Verify(), "The given nodes is not a connected graph"
		self.alloc = sum([n.size for n in nodes])
		self.reduce = sum([int(e.reload * e.begin.size) for e in self.edges])

	def Verify(self):
		if len(self.nodes) == 1:
			return True
		all_nodes = self.nodes.copy()
		while all_nodes:
			n = all_nodes.pop()
			valid = False
			all_edges = n.outE + n.inE
			for e in (n.outE + n.inE):
				if e.end in self.nodes:
					if e.end in all_nodes:
						all_nodes.remove(e.end)
					valid = True
				elif e.begin in self.nodes:
					if e.begin in all_nodes:
						all_nodes.remove(e.begin)
					valid = True
			if not valid:
				return False
		return True

	def __repr__(self):
		#return "Cost: {:6.2f}, Occupy: {:10,}, Reduce: {:10,}, Nodes: {}, In: {}, Out: {}".format(
		return "Cost: {:6.2f}, Occupy: {:10,}, Reduce: {:10,}, Nodes: {}".format(
			(self.reduce * 1.0 / self.alloc), self.alloc, self.reduce,
			[n.idx for n in self.nodes])

class Analyzer(AnalyzerBase):
	def __init__(self, graph_name, buf_size):
		super().__init__(graph_name, buf_size)
		self.next = [Cluster([x]) for x in self.g.GetNodes()]
		self.clusters = self.next
	def BuildCluster(self):
		cur_round = self.next.copy()
		self.next = []
		while cur_round:
			x = cur_round.pop()
			available_size = self.buf_size - x.alloc
			assert available_size > 0, "No buffer size"
			in_candidate = [e.begin for e in x.in_edges]
			max_cost = 0
			max_candidate = None
			for c in in_candidate:
				if c.size > available_size:
					continue
				alloc_c = c.size
				reduce_c = sum([int(e.reload * c.size) for e in c.outE])
				cost_c = Cost(alloc_c, reduce_c)
				if max_cost < cost_c:
					max_cost = cost_c
					max_candidate = c
					max_config = (alloc_c, reduce_c)
			if max_candidate:
				new_nodes = x.nodes
				new_nodes.append(max_candidate)
				new_candidate = Cluster(new_nodes)
				self.clusters.append(new_candidate)
				cur_round.append(new_candidate)

	def CleanUpByCluster(self, x, all_clusters):
		for c in all_clusters:
			for n in c.nodes:
				if n in x.nodes:
					if c in all_clusters:
						all_clusters.remove(c)

	def IsDependent(self, x, c):
		for n in c.nodes:
			if n in x.nodes:
				return True
		return False
	
	def IsAdjcent(self, nodes, c):
		for n in c.nodes:
			for e in (n.inE + n.outE):
				if e.begin in nodes or e.end in nodes:
					return True
		return False
	
	def TryMergeCluster(self):
		self.clusters.sort(key=lambda x: Cost(x.alloc, x.reduce), reverse=True)
		for c in self.clusters:
			print(c)
		all_clusters = self.clusters.copy()
		avilable_size = self.buf_size
		self.sol = []
		self.sol_nodes = []
		self.sol_reduce = 0
		while avilable_size and all_clusters:
			x = all_clusters.pop(0)
			if avilable_size < x.alloc:
				continue
			if self.IsAdjcent(self.sol_nodes, x):
				print("{} IsAdjcent to {}".format(x, [n.idx for n in self.sol_nodes]))
				avilable_size -= x.alloc
			self.sol.append(x)
			self.sol_nodes += x.nodes
			self.sol_reduce += x.reduce
			self.CleanUpByCluster(x, all_clusters)
			print(x)
			print("sol_nodes: ", [n.idx for n in self.sol_nodes])
			print("sol_reduce: ", self.sol_reduce)
		print("sol:")
		i = 0
		for s in self.sol:
			i += 1
			print("{}: {}".format(i, [n.idx for n in s.nodes]))
		print("reduce: {:15,}".format(self.sol_reduce))
		print("alloc: {:4.3f}".format((1.0 * (self.buf_size - avilable_size) / self.buf_size)))
	def Run(self):
		self.BuildCluster()
		self.TryMergeCluster()
		
if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("given a number of buffer size (MB)")
		exit(1)
	buf_size = int(float(sys.argv[1]) * 1024 * 1024)
	ana = Analyzer("rand.graph", buf_size)
	print(ana.Run())
	#for c in ana.clusters:
	#	print(c)
