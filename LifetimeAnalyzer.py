#!/usr/bin/env python3
from AnalyzerBase import AnalyzerBase
import sys

class LifetimeAnalyzer(AnalyzerBase):
    def __init__(self, graph="rand_graph.dot",
                 cmdScheduler="BasicCommandScheduler"):
        super().__init__(graph)
        self.name="LifetimeAnalyzer"
        self.GetRes(cmdScheduler)
        self.cmdSeq=self.analysis[cmdScheduler]['cmdSeq']
        self.res['lifetime'] = {}
    def Run(self):
        for n in self.g.nodes:
            start = self.cmdSeq.index(n.idx)
            assert start is not None
            end = -1
            for e in n.outE:
                out_pos = self.cmdSeq.index(e.end.idx)
                assert out_pos is not None
                if out_pos > end:
                    end = out_pos
            self.res['lifetime'][n.idx] = (start, end)
        return self.res

if __name__ == "__main__":
    ana = LifetimeAnalyzer()
    print(ana.Run())
    ana.SaveRes()
