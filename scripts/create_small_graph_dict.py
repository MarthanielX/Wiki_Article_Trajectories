import networkx as nx
import requests
import json
import matplotlib.pyplot as plt
import statistics
import pandas as pd
import pickle

with open('./data-small/class_lists_small.pkl', 'rb') as f:
    lsts = pickle.load(f)

titles = [item for sublist in lsts for item in sublist]
assert(len(titles) == 600)

with open('./data/directed_network_dictionary.pkl', 'rb') as f:
    directed_graphs = pickle.load(f)

small_dct = {title: directed_graphs[title] for title in titles}

with open('./data-small/directed_network_dict_small.pkl', 'wb') as f:
    pickle.dump(small_dct, f)

