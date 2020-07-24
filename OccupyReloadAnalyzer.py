#!/usr/bin/env python3
from AnalyzerBase import AnalyzerBase
import sys
import math

CHUNK_SIZE = 512 * 1024 # 1KB

class OccupyReloadAnalyzer(AnalyzerBase):
    def __init__(self,
                 graph="rand_graph.dot",
                 lifetimeAnalyzer="LifetimeAnalyzer"):
        super().__init__(graph)
        self.name = "OccupyReloadAnalyzer"
        self.GetRes(lifetimeAnalyzer)
        self.lifetime = self.analysis[lifetimeAnalyzer]['lifetime']
        self.res['OccReload'] = []
    def Run(self):
        for n in self.g.nodes:
            occupSize = n.size
            reloadSize = 0
            s, e = self.lifetime[str(n.idx)]
            lifetime = (e - s) + 1
            for e in n.outE:
                reloadSize += e.reload * occupSize
            ratio = reloadSize / (occupSize * lifetime)
            self.res['OccReload'].append((n.idx, ratio, occupSize, reloadSize))
        self.res['OccReload'].sort(reverse=True, key=lambda x: x[1])
        return self.res

if __name__ == "__main__":
    ana = OccupyReloadAnalyzer()
    print(ana.Run())
    ana.SaveRes()
