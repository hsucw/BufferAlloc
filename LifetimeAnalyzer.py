#!/usr/bin/env python3
from AnalyzerBase import AnalyzerBase
import sys

class LifetimeAnalyzer(AnalyzerBase):
    def __init__(self, graph="rand_graph.dot",
                 cmdScheduler="BasicCommandScheduler"):
        super().__init__(graph)
        self.name="LifetimeAnalyzer"
        self.GetRes(cmdScheduler)
        self.cmdScheduler=cmdScheduler
    def Run(self):
        print(self.analysis)
        return self.res

if __name__ == "__main__":
    ana = LifetimeAnalyzer()
    print(ana.Run())
    ana.SaveRes()
