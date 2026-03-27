import pickle

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

def predict_role(text):
    vec = vectorizer.transform([text])
    return model.predict(vec)[0]