import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

df = pd.read_csv("boli_simptome.csv")

df["simptome"] = df["simptome"].astype(str).fillna('')

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["simptome"])

disease_names = df["boli"].tolist()

def identify_disease(symptoms):
    symptoms = [" ".join(symptoms).lower()]
    user_vector = vectorizer.transform(symptoms)
    similarities = cosine_similarity(user_vector, X)

    top_3_indices = np.argsort(similarities[0])[-3:][::-1]

    top_3_diseases = [disease_names[i] for i in top_3_indices]

    result_string = ",".join(top_3_diseases)

    return result_string, [similarities[0][i] for i in top_3_indices]