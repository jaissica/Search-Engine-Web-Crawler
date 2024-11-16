import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn import tree
from sklearn.metrics import roc_auc_score
import numpy as np


class MyDf2:

    def __init__(self, id, text, label, split):
        self.id = id
        self.text = text
        self.label = label
        self.split = split
        self.df = pd.DataFrame({"id": self.id, "text": self.text, "label": self.label, "split": self.split})
        self.train_data = self.df[self.df["split"] == "train"]["text"].copy()
        self.test_data = self.df[self.df["split"] == "test"]["text"].copy()
        self.train_label = self.df[self.df["split"] == "train"]["label"].copy()
        self.test_label = self.df[self.df["split"] == "test"]["label"].copy()
        self.test_set = pd.DataFrame(
            {"id": ["inmail.{}".format(i) for i in list(self.test_data.index)],
             "text": list(self.test_data), "label": list(self.test_label)})
        self.vectorizer = CountVectorizer(analyzer="word", min_df=0.001, max_df=0.995)
        self.fitted_train_data = self.vectorizer.fit_transform(self.train_data)
        # cannot use fit for test data, otherwise we're cheating
        self.transformed_test_data = self.vectorizer.transform(self.test_data)

    def lr(self):
        # linear regression
        log = LogisticRegression(max_iter=3000)
        log.fit(self.fitted_train_data, self.train_label)
        predict = log.predict(self.transformed_test_data)
        self.test_set["predict"] = predict
        self.output_result(self.test_set.sort_values(by="predict", ascending=False).head(20), "logistic")
        print("ROC AUC score of lg", roc_auc_score(np.array(self.test_label), predict))

    def mnb(self):
        # naive bayes
        mnb = MultinomialNB()
        mnb.fit(self.fitted_train_data, self.train_label)
        predict = mnb.predict_proba(self.transformed_test_data)
        predict = [predict[i, 1] for i in range(len(predict))]
        self.test_set["predict"] = predict
        self.output_result(self.test_set.sort_values(by="predict", ascending=False).head(20), "naive")
        print("ROC AUC score of mnb", roc_auc_score(np.array(self.test_label), predict))

    def dt(self):
        # decision tree
        decision_tree = tree.DecisionTreeClassifier()
        decision_tree.fit(self.fitted_train_data, self.train_label)
        predict = decision_tree.predict_proba(self.transformed_test_data)
        predict = [predict[i, 1] for i in range(len(predict))]
        self.test_set["predict"] = predict
        self.test_set.sort_values(by="predict", ascending=False).head(10)
        self.output_result(self.test_set.sort_values(by="predict", ascending=False).head(20), "decision")
        print("ROC AUC score of dt", roc_auc_score(np.array(self.test_label), predict))

    def output_result(self, df, name):
        id = list(df["id"])
        spam = list(df["label"])
        predict = list(df["predict"])
        with open("./output/{}.txt".format(name), "a") as f:
            f.write("{:>12} {:>5} {:>8}\n".format("id", "spam", "predict"))
            for idx, value in enumerate(id):
                line = "{:>12} {:>5} {:>8}\n".format(value, spam[idx], "{:.10f}".format(predict[idx]))
                f.write(line)


