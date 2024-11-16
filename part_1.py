import pandas as pd
from sklearn import linear_model
from sklearn.naive_bayes import MultinomialNB
from sklearn import tree


class MyDf:

    def __init__(self, ids, features, spam, split):
        self.ids = ids
        self.features_name = []
        self.features = []
        self.df = pd.DataFrame()
        self.train_set = pd.DataFrame()
        self.test_set = pd.DataFrame()
        self.spam = spam
        self.split = split
        self.initialize(features)
        self.get_df()

    def initialize(self, features):
        for word in features:
            self.features_name.append(word)
            temp = []
            for id in self.ids:
                if id in features[word]:
                    temp.append(features[word][id])
                else:
                    temp.append(0)
            self.features.append(temp)

    def get_df(self):
        df_data = {"id": self.ids}
        for word in self.features_name:
            df_data[word] = self.features.pop(0)
        df_data["label"] = list(map(lambda x: 1 if self.spam[x] == "spam" else 0, self.spam))
        df_data["split"] = [self.split[i] for i in self.split]
        self.df = pd.DataFrame(df_data)
        self.train_set = self.df[self.df["split"] == "train"].copy()
        self.test_set = self.df[self.df["split"] == "test"].copy()
        self.test_set["predict"] = 0


    def lr(self):
        # linear regression
        reg = linear_model.LinearRegression()
        reg.fit(self.train_set.iloc[:, 1:-2], self.train_set.iloc[:, -2])
        self.test_set["predict"] = reg.predict(self.test_set.iloc[:, 1:-3])
        self.output_result(self.test_set.sort_values(by="predict", ascending=False).head(20), "linear")

    def mnb(self):
        # naive bayes
        mnb = MultinomialNB()
        mnb.fit(self.train_set.iloc[:, 1:-2], self.train_set.iloc[:, -2])
        predict = mnb.predict_proba(self.test_set.iloc[:, 1:-3])
        predict = [predict[i, 1] for i in range(len(predict))]
        self.test_set["predict"] = predict
        self.output_result(self.test_set.sort_values(by="predict", ascending=False).head(20), "naive")


    def dt(self):
        # decision tree
        decision_tree = tree.DecisionTreeClassifier()
        decision_tree.fit(self.train_set.iloc[:, 1:-2], self.train_set.iloc[:, -2])
        predict = decision_tree.predict_proba(self.test_set.iloc[:, 1:-3])
        self.test_set["predict"] = [predict[i, 1] for i in range(len(predict))]

        self.output_result(self.test_set.sort_values(by="predict", ascending=False).head(20), "decision")

    def output_result(self, df, name):
        id = list(df["id"])
        spam = list(df["label"])
        predict = list(df["predict"])
        with open("./output/{}.txt".format(name), "a") as f:
            f.write("{:>12} {:>5} {:>8}\n".format("id", "spam", "predict"))
            for idx, value in enumerate(id):
                line = "{:>12} {:>5} {:>8}\n".format(value, spam[idx], "{:.5f}".format(predict[idx]))
                f.write(line)





