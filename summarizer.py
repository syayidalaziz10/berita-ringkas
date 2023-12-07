import nltk
import pandas as pd
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')
nltk.download("stopwords")


def generate_summary(news_text, num_sentences):
    kalimat = nltk.sent_tokenize(news_text)

    # tfidf
    tfidf_vectorizer = TfidfVectorizer()
    tfidf = tfidf_vectorizer.fit_transform(kalimat)
    terms = tfidf_vectorizer.get_feature_names_out()
    tfidf = pd.DataFrame(data=tfidf.toarray(), columns=terms)

    # cosine-similarity
    cosine = cosine_similarity(tfidf, tfidf)
    similarity = pd.DataFrame(cosine, columns=range(
        len(kalimat)), index=range(len(kalimat)))

    # graph
    G = nx.DiGraph()

    for i in range(len(cosine)):
        G.add_node(i)

    for i in range(len(cosine)):
        for j in range(len(cosine)):
            similarity = cosine[i][j]
            if similarity > 0.1 and i != j:
                G.add_edge(i, j)

    closeness = nx.closeness_centrality(G)
    sorted_closeness = sorted(
        closeness.items(), key=lambda x: x[1], reverse=True)

    hasil_ringkasan = ""
    for node, closeness in sorted_closeness[:num_sentences]:
        top_sentence = kalimat[node]
        hasil_ringkasan += top_sentence + " "

    return hasil_ringkasan
