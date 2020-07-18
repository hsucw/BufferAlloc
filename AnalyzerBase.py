#!/usr/bin/env python3
from Graph import Node
from Graph import Edge
from Graph import Graph

from random import random
import jsonpickle
import sys
sys.setrecursionlimit(9000000)

class AnalyzerBase():
	def __init__(self, graph_name, buf_size):
		with open(graph_name, 'r') as outf:
			frozen = outf.read()
		self.g = jsonpickle.decode(frozen)
		self.buf_size = buf_size
	def Run(self):
		print("not yet implement")
		return (self.buf_size, [])
