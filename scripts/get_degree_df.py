import networkx as nx
import requests
import json
import matplotlib.pyplot as plt
import statistics

import pandas as pd
import pickle
import math


def construct_row(title):

    graph = graph_dict[title]
    degrees = sorted([deg for node, deg in graph.degree])[::-1]
    n = len(degrees)
    lst = []

    ["T5 Avg Deg", "T10 Avg Deg", "T5% Avg Deg", "T10% Avg Deg", "Count Deg>5", "Count Deg>10"]

    lst.append( statistics.mean(degrees[:min(n, 5)]))
    lst.append( statistics.mean(degrees[:min(n, 10)]))

    lst.append( statistics.mean(degrees[: n//20 ]))
    lst.append( statistics.mean(degrees[: n//10 ]))

    lst.append( count([x for x in lst if x > 5]) )
    lst.append( count([x for x in lst if x > 10]) )

    return lst

def construct_dataframe(titles, directed):

    cols = ["T5 Avg Deg", "T10 Avg Deg", "T5% Avg Deg", "T10% Avg Deg", "Count Deg>5", "Count Deg>10"]
    row_lst = []
    for i, title in enumerate(titles):
        print(i, title)
        row_lst.append(construct_row(title))

    return pd.DataFrame(row_lst, columns = ['title', *cols] ).set_index('title')

directed = False

with open('../data/random5000_article_graphs.pkl', 'rb') as f:
  graph_dict = pickle.load(f)

with open('../data/random5000_article_titles.pkl', 'rb') as f:
  class_lists = pickle.load(f)

titles = [item for sublist in class_lists for item in sublist]

df = construct_dataframe(titles, directed)

with open('../data/df_undirected_stats_random5000.pkl', 'wb') as f:
  pickle.dump(df, f)
