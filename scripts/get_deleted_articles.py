import networkx as nx
import requests
import json
import statistics
import pickle
import math

with open('./data/directed_network_dictionary.pkl', 'rb') as f:
    directed_graphs = pickle.load(f)

lst = [x for x in directed_graphs if directed_graphs[x].order() == 0]

for x in lst:
    print(x)

with open('./data/deleted_articles.pkl', 'wb') as f:
    pickle.dump(lst, f)
