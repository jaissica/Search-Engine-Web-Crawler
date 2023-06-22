import numpy as np
import math

#3
class WT2GPageRanking:

    def __init__(self, path):
        self.path = path
        self.M = {}
        self.P = []
        self.N = 0
        self.out_links = {}

        self.S = []
        self.L = {}
        self.d = 0.85
        self.PR = {}

        self.initialize()

    def initialize(self):
        self.read_txt()
        self.P = [i for i in self.M]
        self.N = len(self.P)
        self.get_out_links()
        self.get_S()
        self.get_L()

    def get_page_rank(self):
        for i in self.P:
            self.PR[i] = 1/self.N

        newPR = {}
        perplexity = 0
        unit_no_change = 0
        while True:
            sinkPR = 0
            for p in self.S:
                sinkPR += self.PR[p]
            for p in self.P:
                newPR[p] = (1 - self.d) / self.N
                newPR[p] += self.d * sinkPR / self.N
                for q in self.M[p]:
                    newPR[p] += self.d * self.PR[q] / self.L[q]
            for p in self.P:
                self.PR[p] = newPR[p]
            new_perplexity = 2 ** (-np.sum([self.PR[x]*math.log(self.PR[x], 2) for x in self.PR]))
            if int(perplexity) % 10 == int(new_perplexity) % 10:
                unit_no_change += 1
            else:
                unit_no_change = 0
            perplexity = new_perplexity
            print(unit_no_change, perplexity)
            if unit_no_change == 4:
                return

    def get_out_links(self):
        for c in self.M:
            if self.M[c]:
                for p in self.M[c]:
                    if p not in self.out_links:
                        self.out_links[p] = [c]
                    else:
                        self.out_links[p].append(c)

    def get_S(self):
        for p in self.P:
            if p not in self.out_links:
                self.S.append(p)

    def get_L(self):
        for p in self.P:
            if p in self.out_links:
                self.L[p] = len(self.out_links[p])
            else:
                self.L[p] = 0

    def read_txt(self):
        with open(self.path, "r") as f:
            for line in f.readlines():
                new_line = line.replace(" \n", "")
                new_line = new_line.replace("\n", "")
                new_line = new_line.split(" ")
                if len(new_line) == 1:
                    self.M[new_line[0]] = []
                else:
                    self.M[new_line[0]] = list(set(new_line[1:]))

    def print_top_500(self):
        final = sorted(self.PR, key=self.PR.get, reverse=True)[:500]
        adjust = 25
        lines = [[str(p).ljust(adjust), str(self.PR[p]).ljust(adjust), str(self.L[p]).ljust(adjust),
                  str(len(self.M[p])).ljust(adjust)] for p in final]
        headers = ['Page'.ljust(adjust), 'Page Rank'.ljust(adjust), 'No. of Outlinks'.ljust(adjust),
                   'No. of Inlinks'.ljust(adjust)]
        with open('./wt2g/wt2g_page_ranking.txt', "a") as f:
            f.write(''.join(headers))
            f.write("\n")
            for l in lines:
                f.write(''.join(l))
                f.write('\n')


wt2g = WT2GPageRanking("wt2g/wt2g_inlinks.txt")
wt2g.get_page_rank()
wt2g.print_top_500()
