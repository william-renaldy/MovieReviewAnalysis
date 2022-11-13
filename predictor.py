import pickle
import nltk
import re
import tensorflow as tf
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from keras.models import load_model,Model

try:
    stopwords.words("english")
except LookupError:
    nltk.download("stopwords")


class Processor():
    def __init__(self):
        self.ps = PorterStemmer()

        with open("vectorizer.pkl","rb") as f:
            self.Tfidf = pickle.load(f)

        self.corpus = []

        self.X = None


    def pre_process(self,data):
        self.corpus = []

        for i in range(len(data)):
            review = re.sub("[^a-zA-Z]"," ",data[i])

            review = review.lower().split()

            review = [self.ps.stem(r) for r in review if r not in stopwords.words("english")]

            review = " ".join(review)

            self.corpus.append(review)

        self.X = self.Tfidf.transform(self.corpus).toarray()

        return self.X

        




class Model():
    def __init__(self):
        self.model = load_model("keras-model8")

    
    def load_model(self):
        return self.model



    def predict(self,X):

        res = self.model.predict(X)

        res = [round(float(i)) for i in res]

        return res




if __name__ == "__main__":
    message = "Great movie ever seen"

    X = Processor().pre_process([message,"worst movie"])

    model = Model()


    print(model.predict(X))