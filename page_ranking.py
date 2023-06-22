import numpy as np
import math
import os

#2
class PageRanking():

    def __init__(self):
        self.M = {}
        self.P = []
        self.N = 0
        self.outlinks = {}
        self.S = []
        self.L = {}
        self.d = 0.85
        self.PR = {}
        self.initialization()


    def initialization(self):
        self.read_inlinks()
        self.read_outlinks()
        self.P = [i for i in self.M]
        self.N = len(self.P)
        self.get_S()
        self.get_L()



    def get_page_rank(self):
        for i in self.P:
            self.PR[i] = 1/self.N
        newPR = {}
        perplexity = 0
        loops = 0
        unit_no_change = 0
        while True:
            loops += 1
            print(loops)
            sinkPR = 0
            for p in self.S:
                sinkPR += self.PR[p]
            for p in self.P:
                # 80% * sum(I(Ai) / out_degree(Ai)) + 20% * 1 / the # of pages
                newPR[p] = (1 - self.d) / self.N
                newPR[p] += self.d * sinkPR / self.N
                for q in self.M[p]:
                    # sum(I(Ai) / out_degree(Ai)), all the importance
                    try:
                        if p in self.PR:
                            newPR[p] += self.d * self.PR[q] / self.L[q]
                    except:
                        pass
            for p in self.P:
                self.PR[p] = newPR[p]
            new_perplexity = 2 ** (-np.sum([self.PR[x] * math.log(self.PR[x], 2) for x in self.PR]))
            if int(perplexity) % 10 == int(new_perplexity) % 10:
                unit_no_change += 1
            else:
                unit_no_change = 0
            perplexity = new_perplexity
            print(unit_no_change, perplexity)
            if unit_no_change == 4:
                return


    def get_S(self):
        for p in self.P:
            if p not in self.outlinks:
                self.S.append(p)



    def get_L(self):
        for p in self.P:
            if p in self.outlinks:
                self.L[p] = len(self.outlinks[p])
            else:
                self.L[p] = 0




    def print_top_500(self):
        if os.path.exists("links/page_ranking.txt"):
            os.remove("links/page_ranking.txt")
        final = sorted(self.PR, key=self.PR.get, reverse=True)[:500]
        adjust = 100
        lines = [[p.ljust(adjust), str(self.PR[p]).ljust(adjust), str(self.L[p]).ljust(adjust),
                  str(len(self.M[p])).ljust(adjust)] for p in final]
        headers = ['Page'.ljust(adjust), 'Page Rank'.ljust(adjust), 'No. of Outlinks'.ljust(adjust),
                   'No. of Inlinks'.ljust(adjust)]
        with open('links/page_ranking.txt', "a") as f:
            f.write(''.join(headers))
            f.write("\n")
            for l in lines:
                print(l)
                f.write(''.join(l))
                f.write('\n')


    def read_inlinks(self):
        print("inlink")
        with open("links/inlinks.txt", "r") as f:
            for line in f.readlines():
                new_line = line.replace(" \n", "")
                new_line = new_line.replace("\n", "")
                new_line = new_line.split(" ")
                if len(new_line) == 1:
                    self.M[new_line[0]] = []
                else:
                    self.M[new_line[0]] = new_line[1:]



    def read_outlinks(self):
        print("outlink")
        with open("links/outlinks.txt", "r", encoding="utf-8") as f:
            for line in f.readlines():
                new_line = line.replace(" \n", "")
                new_line = new_line.replace("\n", "")
                new_line = new_line.split(" ")
                if len(new_line) == 1:
                    self.outlinks[new_line[0]] = []
                else:
                    self.outlinks[new_line[0]] = new_line[1:]



pr = PageRanking()
pr.initialization()
pr.get_page_rank()
pr.print_top_500()
