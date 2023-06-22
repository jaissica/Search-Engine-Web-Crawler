import sys, getopt
import matplotlib.pyplot as plt
import math


class TrecEval:

    def __init__(self, qrel_file, trec_file, print_all_queries, graph):
        self.qrel = {}
        self.qrel_raw = {}
        self.num_rel = {}
        self.trec = {}
        self.recalls = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        self.cutoffs = [5, 10, 15, 20, 30, 100, 200, 500, 1000]
        self.print_all_queries = print_all_queries
        self.trec_file = trec_file
        self.qrel_file = qrel_file
        self.qrel_raw_file = "qrel_raw.txt"
        self.graph = graph

    def get_qrel(self):
        with open(self.qrel_file, "r") as f:
            for line in f.readlines():
                line = line.replace("\n", "")
                query_id, name, doc_id, grade = line.split(" ")
                grade = float(grade)
                if query_id in self.qrel:
                    self.qrel[query_id][doc_id] = grade
                else:
                    self.qrel[query_id] = {}
                    self.qrel[query_id][doc_id] = grade

                if query_id in self.num_rel:
                    self.num_rel[query_id] += grade
                else:
                    self.num_rel[query_id] = 0
                    self.num_rel[query_id] += grade

    def get_qrel_raw(self):
        with open(self.qrel_raw_file, "r") as f:
            for line in f.readlines():
                line = line.replace("\n", "")
                query_id, name, doc_id, grade = line.split(" ")
                grade = float(grade)
                if query_id in self.qrel_raw:
                    self.qrel_raw[query_id][doc_id] = grade
                else:
                    self.qrel_raw[query_id] = {}
                    self.qrel_raw[query_id][doc_id] = grade

                if query_id in self.num_rel:
                    self.num_rel[query_id] += grade
                else:
                    self.num_rel[query_id] = 0
                    self.num_rel[query_id] += grade

    def get_trec(self):
        with open(self.trec_file, "r") as f:
            for line in f.readlines():
                line = line.replace("\n", "")
                query_id, Q0, doc_id, rank, score, Exp = line.split(" ")
                score = float(score)
                if query_id in self.trec:
                    self.trec[query_id][doc_id] = score
                else:
                    self.trec[query_id] = {}
                    self.trec[query_id][doc_id] = score

    def calculate(self):
        self.get_trec()
        self.get_qrel()

        tot_num_ret = 0
        tot_num_rel = 0
        tot_num_rel_ret = 0
        num_queries = 0
        sum_prec_at_cutoffs = {}
        sum_prec_at_recalls = {}
        sum_avg_prec = 0
        sum_r_prec = 0
        avg_prec_at_cutoffs = {}
        avg_prec_at_recalls = {}
        for query_id in sorted(self.trec.keys(), key=int):
            if self.num_rel[query_id] == 0:
                continue

            num_queries += 1  # record how many queries have been processed

            prec_list = {}
            rec_list = {}

            num_ret = 0  # number retrieved
            num_rel_ret = 0  # number relevant retrieved
            sum_prec = 0  # sum precision

            # issue: if we don't break ties lexicographically, the results vary a little
            for doc_id in sorted(self.trec[query_id], key=lambda x: (self.trec[query_id].get(x), x), reverse=True):
                num_ret += 1  # the number of retrieved docs
                if doc_id in self.qrel[query_id]:
                    rel = self.qrel[query_id][doc_id]
                else:
                    rel = 0
                if rel:
                    sum_prec += rel * (1.0 + num_rel_ret) / num_ret  # if rel=1, then add to sum
                    num_rel_ret += rel  # update the number of retrieved relevant docs

                prec_list[num_ret] = num_rel_ret / num_ret
                rec_list[num_ret] = num_rel_ret / self.num_rel[query_id]
                if num_ret >= 1000:
                    break

            # precision-recall plot
            if self.graph:
                plt.figure()
                x = [rec_list[i] for i in rec_list]
                y = [prec_list[i] for i in prec_list]
                plt.plot(x, y, '-')
                plt.ylabel("Precision")
                plt.xlabel("Recall")
                plt.title("Precision-Recall Plot, Query ID: {}".format(query_id))
                plt.show()

            avg_prec = sum_prec / self.num_rel[query_id]

            # in case there are less than 1000 docs for a query
            # pretend the rest docs (1000 - num_ret) are all non-relevant
            final_recall = num_rel_ret / self.num_rel[query_id]
            i = num_ret + 1
            while i <= 1000:
                prec_list[i] = num_rel_ret / i
                rec_list[i] = final_recall
                i += 1

            prec_at_cutoffs = {}
            for cutoff in self.cutoffs:
                prec_at_cutoffs[cutoff] = prec_list[cutoff]

            if self.num_rel[query_id] > num_ret:
                r_prec = num_rel_ret / self.num_rel[query_id]  # num_rel_ret is at most 1000
            else:
                int_num_rel = int(self.num_rel[query_id])
                frac_num_rel = self.num_rel[query_id] - int_num_rel

                if frac_num_rel > 0:
                    r_prec = (1 - frac_num_rel) * prec_list[int_num_rel] + frac_num_rel * prec_list[int_num_rel + 1]
                else:
                    r_prec = prec_list[int_num_rel]

            max_prec = 0
            for i in reversed(range(1, 1001)):
                if prec_list[i] > max_prec:
                    max_prec = prec_list[i]
                else:
                    prec_list[i] = max_prec

            prec_at_recalls = {}
            i = 1
            for recall in self.recalls:
                while i <= 1000 and rec_list[i] < recall:
                    i += 1
                if i <= 1000:
                    prec_at_recalls[recall] = prec_list[i]
                else:
                    prec_at_recalls[recall] = 0

            if self.print_all_queries:
                self.eval_print(query_id, num_ret, self.num_rel[query_id], num_rel_ret, prec_at_recalls, avg_prec,
                                prec_at_cutoffs, r_prec)

            tot_num_ret += num_ret
            tot_num_rel += self.num_rel[query_id]
            tot_num_rel_ret += num_rel_ret

            for cutoff in self.cutoffs:
                if cutoff in sum_prec_at_cutoffs:
                    sum_prec_at_cutoffs[cutoff] += prec_at_cutoffs[cutoff]
                else:
                    sum_prec_at_cutoffs[cutoff] = 0
                    sum_prec_at_cutoffs[cutoff] += prec_at_cutoffs[cutoff]
            for recall in self.recalls:
                if recall in sum_prec_at_recalls:
                    sum_prec_at_recalls[recall] += prec_at_recalls[recall]
                else:
                    sum_prec_at_recalls[recall] = 0
                    sum_prec_at_recalls[recall] += prec_at_recalls[recall]
            sum_avg_prec += avg_prec
            sum_r_prec += r_prec

        for cutoff in self.cutoffs:
            avg_prec_at_cutoffs[cutoff] = sum_prec_at_cutoffs[cutoff] / num_queries
        for recall in self.recalls:
            avg_prec_at_recalls[recall] = sum_prec_at_recalls[recall] / num_queries

        mean_avg_prec = sum_avg_prec / num_queries
        avg_r_prec = sum_r_prec / num_queries

        self.eval_print(num_queries, tot_num_ret, tot_num_rel, tot_num_rel_ret, avg_prec_at_recalls, mean_avg_prec,
                        avg_prec_at_cutoffs, avg_r_prec)

    def eval_print(self, query_id, num_ret, num_rel, num_rel_ret, prec_at_recalls, avg_prec, prec_at_cutoffs, r_prec):
        print("Queryid (Num):     {}".format(query_id))
        print("Total number of documents over all queries")
        print("    Retrieved:    {}".format(num_ret))
        print("    Relevant:     {:.0f}".format(num_rel))
        print("    Rel_ret:      {:.0f}".format(num_rel_ret))
        print("Interpolated Recall - Precision Averages:")
        for p in prec_at_recalls:
            print("    at {:.2f}       {:.4f}".format(p, prec_at_recalls[p]))
        print("Average precision (non-interpolated) for all rel docs(averaged over queries)")
        print("                  {:.4f}".format(avg_prec))
        print("Precision:")
        for p in prec_at_cutoffs:
            print("  At {:4} docs:   {:.4f}".format(p, prec_at_cutoffs[p]))
        print("R-Precision (precision after R (= num_rel for a query) docs retrieved):")
        print("    Exact:        {:.4f}".format(r_prec))
        print("")

    def compute_ndcg(self, rank):
        self.get_trec()
        self.get_qrel_raw()
        for query_id in self.trec:
            i = 1
            cumulative_gain = 0
            ordering = {}
            for doc in self.trec[query_id]:
                if doc in self.qrel[query_id]:
                    rel = self.qrel[query_id][doc]
                else:
                    rel = 0
                ordering[doc] = rel
                gain = 2 ** rel - 1
                discount = 1 / (math.log(1 + i))
                cumulative_gain += gain * discount
                if i == rank:
                    break
                else:
                    i += 1
            ideal_ordering = {key: ordering[key] for key in sorted(ordering, key=ordering.get, reverse=True)}
            ideal_cumulative_gain = 0
            for idx, doc in enumerate(ideal_ordering):
                gain = 2 ** ideal_ordering[doc] - 1
                discount = 1 * (math.log(1 + idx + 1))
                ideal_cumulative_gain += gain / discount
            ndcg = cumulative_gain / ideal_cumulative_gain
            print("Query ID: {} nDCG: {:.4f} At rank: {}".format(query_id, ndcg, rank))



my_trec = TrecEval("qrel_raw.txt", "output_gen.txt", 1, 1)
my_trec.calculate()
my_trec.compute_ndcg(10)

