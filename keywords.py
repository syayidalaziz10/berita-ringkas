import pandas as pd
import nltk
import re
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter


nltk.download('punkt')
nltk.download("stopwords")


def generate_keywords(news_text, num_keyword):

    news_text = re.sub(r'\d+', '', news_text)
    news_text = re.sub(r'[^\w\s.]', '', news_text)
    news_text = news_text.lower()

    stop_words = set(stopwords.words('indonesian'))
    words = news_text.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]

    news_text = ' '.join(filtered_words)

    kata = word_tokenize(news_text)
    kata = [k.lower() for k in kata if k != '.']
    kata = list(set(kata))

    kalimat = nltk.sent_tokenize(news_text)
    kalimat = [sentence.replace('.', '') for sentence in kalimat]

    matrikskata = pd.DataFrame(0, index=kata, columns=kata)

    for sent in kalimat:
        kata_kalimat = word_tokenize(sent)
        for i in range(len(kata_kalimat)-1):
            # jika kata pada sebelah kanan
            matrikskata.at[kata_kalimat[i], kata_kalimat[i+1]] += 1
            # jika kata pada sebelah kiri
            matrikskata.at[kata_kalimat[i+1], kata_kalimat[i]] += 1

    cosine = cosine_similarity(matrikskata, matrikskata)
    similarity = pd.DataFrame(
        cosine, columns=matrikskata.index, index=matrikskata.index)

    G = nx.DiGraph()
    for i in range(len(cosine)):
        G.add_node(i)

    for i in range(len(cosine)):
        for j in range(len(cosine)):
            similarity = cosine[i][j]
            if similarity > 0.1 and i != j:
                G.add_edge(i, j)

    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color='b')
    nx.draw_networkx_edges(G, pos, edge_color='red', arrows=True)
    nx.draw_networkx_labels(G, pos)

    plt.show()

    pagerank = nx.pagerank(G)

    sorted_pagerank = sorted(
        pagerank.items(), key=lambda x: x[1], reverse=True)

    sentence = ""
    for node, pagerank in sorted_pagerank[:num_keyword]:
        top_sentence = kata[node]
        sentence += top_sentence + ", "

    return sentence
