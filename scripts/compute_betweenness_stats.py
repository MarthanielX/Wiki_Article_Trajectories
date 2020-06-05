import pandas as pd
import pickle
import math
import statistics
import networkx as nx

def get_betweenness_list(title):
    g = graph_dict[title].to_undirected()
    return sorted(nx.networkx.algorithms.centrality.betweenness_centrality(g).values(), reverse=True)

def construct_row(title):

    #["T8 Avg Count", "T12 Avg Count", "T15 Avg Count", "Count>2", "Count>4", "Count>7"]
    counts = get_betweenness_list(title)
    lst = [title,]
    n = len(counts)

    # Top i betweenness
    for i in range(1, 5):
        lst.append( statistics.mean(counts[:min(n, i)]))
    for i in range(5, 30, 5):
        lst.append( statistics.mean(counts[:min(n, i)]))

    # top i%
    for i in range(1, 5):
        lst.append( statistics.mean(counts[:max( (i*n)//100, 1)]) )

    for i in range(5, 55, 5):
        lst.append( statistics.mean(counts[:max( (i*n)//100, 1)]) )

    # count > i / 100; .05 - .5
    for i in range(5, 55, 5):
        lst.append( len([x for x in counts if x > i/100 ]) )

    return lst

def construct_dataframe(titles):
    cols = ["T{} Avg Bwn".format(i) for i in range(1, 5)]
    cols += ["T{} Avg Bwn".format(i) for i in range(5, 30, 5)]
    cols += ["T{} Pct Avg Bwn".format(i) for i in range(1, 5)]
    cols += ["T{} Pct Avg Bwn".format(i) for i in range(5, 55, 5)]
    cols += ["Count Bwn > {}/100".format(i) for i in range(5, 55, 5)]

    row_lst = []
    for i, title in enumerate(titles):
        print(i, title)
        row_lst.append(construct_row(title))

    return pd.DataFrame(row_lst, columns = ['title', *cols] ).set_index('title')


with open('../data/article_titles_all.pkl', 'rb') as f:
    class_lists  = pickle.load(f)
titles = [item for sublist in class_lists for item in sublist]

with open('../data/graph_dictionary_all.pkl', 'rb') as f:
    graph_dict = pickle.load(f)

df = construct_dataframe(titles)

with open('../data/df_undirected_betweenness_stats.pkl', 'wb') as f:
    pickle.dump(df, f)
