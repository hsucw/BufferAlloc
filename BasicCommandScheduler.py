#!/usr/bin/env python3
from AnalyzerBase import AnalyzerBase
import sys

class BasicCommandScheduler(AnalyzerBase):
    def __init__(self, graph="rand_graph.dot"):
        super().__init__(graph)
        self.name="BasicCommandScheduler"
    def Run(self):
        commands = [n.idx for n in self.g.GetNodes()]
        commands.sort()
        self.res['cmdSeq'] = commands
        return self.res

if __name__ == "__main__":
    ana = BasicCommandScheduler()
    print(ana.Run())
    ana.SaveRes()
