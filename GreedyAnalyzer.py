#!/usr/bin/env python3
from AnalyzerBase import AnalyzerBase
import sys
import math

CHUNK_SIZE = 512 * 1024 # 1KB

class GreedyAnalyzer(AnalyzerBase):
    def __init__(self,
                 buf_size,
                 graph="rand_graph.dot",
                 cmdScheduler="BasicCommandScheduler",
                 lifetimeAnalyzer="LifetimeAnalyzer",
                 occReloadAnalyzer="OccupyReloadAnalyzer"):
        super().__init__(graph)
        self.name = "GreedyAnalyzer"
        self.buf_size = buf_size
        self.GetRes(lifetimeAnalyzer)
        self.GetRes(cmdScheduler)
        self.GetRes(occReloadAnalyzer)
        self.lifetime = self.analysis[lifetimeAnalyzer]['lifetime']
        self.cmdSeq = self.analysis[cmdScheduler]['cmdSeq']
        self.occReload = self.analysis[occReloadAnalyzer]['OccReload']
        self.res['GreedyBufAlloc'] = {}
    def Run(self):
        occ_status = [0] * len(self.cmdSeq)
        max_reload = 0
        candidate = []
        for n, r, occ, reld in self.occReload:
            pick = True
            occ_origin = occ_status.copy()
            s, e = self.lifetime[str(n)]
            if e == -1:
                continue
            for i in range(s, e + 1):
                occ_status[i] += occ
                if occ_status[i] > self.buf_size:
                    pick = False
                    break
            if not pick:
                occ_status = occ_origin.copy()
            else:
                max_reload += reld
                candidate.append(n)
        print("occ: ", ["{:.2%}".format(float(x / self.buf_size)) for x in occ_status])
        print("max reload: {:,.2f}".format(max_reload))
        self.res['GreedyBufAlloc'] = candidate
        return self.res

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("given a number of buffer size (MB)")
        exit(1)
    buf_size = int(float(sys.argv[1]) * 1024 * 1024)
    ana = GreedyAnalyzer(buf_size)
    print(ana.Run())
    ana.SaveRes()
