# BufferAlloc

This a toy for buffer allocation practice.


## Graph.py
This file contains the basic graph definition.
  - Node
    - idx: unique ID
    - inE: in degree edges
    - outE: out degree edges
    - size: the size of this node
  - Edge
    - idx: unique ID
    - begin: the 'from' node
    - end: the 'to' node
    - reload: the reload times (1X means no additional reload)
  - Graph
    - nodes: nodes in this graph
    - edges: edges in this graph
    
## Builder.py
This file randomly creates nodes by given the number of random objects.
Users also can use this class to craft their own graph
- Builder:
  - GetGraph(self): return current graph
  - PickRandomNode(self): return a node in graph randomly
  - PickRandomNodePair(self):	return two nodes in graph randomly
  - CreateRandomNode(self): create a random nodes that it always be end of the edge connecting it between the original graph. 
  - CreateRandomEdge(self): create a random edges, always satisfy begin.idx < end.idx. If the creation fails, creates a node randomly.

Usage:   
  `./Builder.py 100 rand.graph`
  - *100* means that the total number of random object.
  - rand.graph: optional, output graph name. The default name is "rand.graph".
  
## AnalyszerBase.py
A example analyzer for buffer allocation
- Input: a serialized graph, a buffer size (1MB)
- Output: the nodes should be located in buffer.
- Run(): return the answer

## Analyzer.py
My implementation of buffer allocation
Usage:
  `./Analyzer 1 rand.graph`   
  - *1* means that the total usable buffer size is 1MB.  
  - rand.graph: optional, graph file for analysis. 

#### The answer format:
1. early stage: should a list of nodes.   
Example: [0, 3, 15, 17, ...]
2. mid-term: should be a list of all of nodes in graph, and with alloc/release action.   
  Example: [0: {alloc: [0], release: []}, 1: {alloc: [1], release: [0]}, ...,]
3. long-term: the address within the given buffer.  
  Example: [0: {alloc: [(0, 0x00)], release: []}, 1: {alloc: [(1, 0x40)], release: [0]}, ...,]

## Verifier.py (TODO)
The verification of the answer.
- Input: a answer (including the given buffer size)
- Output: the reduced reload size, the answer is valid or not.


