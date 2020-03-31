# -*- coding: utf-8 -*-
"""Generating Article Trajectory Extensions

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Y92-NJ1gE59bYONwsXr2pnZ3H9SEBw6N
"""

import networkx as nx
import requests
import json
import matplotlib.pyplot as plt
import statistics
import pandas as pd
import pickle
import math

"""# Graph Creation Functions"""

def get_article_revisions(title):
    revisions = []
    # create a base url for the api and then a normal url which is initially
    # just a copy of it
    # The following line is what the requests call is doing, basically.
    # "http://en.wikipedia.org/w/api.php/?action=query&titles={0}&prop=revisions&rvprop=flags|timestamp|user|size|ids&rvlimit=500&format=json&continue=".format(title)
    wp_api_url = "http://en.wikipedia.org/w/api.php/"

    # list_parameters = {'action' : 'query',
    #               'generator' : 'allpages',
    #               'prop' : 'pageassessments',
    #               'rvprop' : 'flags|timestamp|user|size|ids',
    #               'rvlimit' : 500,
    #               'format' : 'json',
    #               'continue' : ''}

    title_parameters = {'action' : 'query',
                  'titles' : title,
                  'prop' : 'revisions',
                  'rvprop' : 'flags|timestamp|user|size|ids',
                  'rvlimit' : 500,
                  'format' : 'json',
                  'continue' : '' }
    while True:
        # the first line open the urls but also handles unicode urls
        call = requests.get(wp_api_url, params=title_parameters)
        # call = requests.get(wp_api_url, params=list_parameters)
        api_answer = call.json()

        # get the list of pages from the json object
        pages = api_answer["query"]["pages"]

        # for every page, (there should always be only one) get its revisions:
        for page in pages.keys():
            if ('revisions' in pages[page]):
                query_revisions = pages[page]["revisions"]

                # Append every revision to the revisions list
                for rev in query_revisions:
                    revisions.append(rev)

        # 'continue' tells us there's more revisions to add
        if 'continue' in api_answer:
            # replace the 'continue' parameter with the contents of the
            # api_answer dictionary.
            title_parameters.update(api_answer['continue'])
            # list_parameters.update(api_answer['continue'])
        else:
            break

    for r in revisions:
      if 'anon' in r:
        r['user'] = "Anon:" + r['user']
      if 'userhidden' in r:
        r['user'] = "Hidden"

    return(revisions)

def create_article_trajectory_graph(revisions, directed=True, weighted=False):
  if directed:
    g = nx.DiGraph()
  else:
    g = nx.Graph()

  for i in range(len(revisions)):
    if weighted:
        if g.has_edge(revisions[i]['user'], revisions[i-1]['user']):
            g[revisions[i]['user']][revisions[i-1]['user']]['count'] += 1
        else:
            g.add_edge(revisions[i]['user'], revisions[i-1]['user'])
            g[revisions[i]['user']][revisions[i-1]['user']]['count'] = 1
    else:
        g.add_edge(revisions[i]['user'], revisions[i-1]['user'])

  return g

with open('./data/class_lists_final.pkl', 'rb') as f:
  lsts = pickle.load(f)

titles = [item for sublist in lsts for item in sublist]
assert(len(titles) == 6000)

with open('./data/directed_network_dictionary.pkl', 'rb') as f:
   directed_graphs = pickle.load(f)

# with open('./data/undirected_network_dictionary.pkl', 'rb') as f:
#    undirected_graphs = pickle.load(f)

#directed_graphs = {}
#undirected_graphs = {}

for i in range(len(titles)):
    title = titles[i]
    print(i, title)
    #if (title not in directed_graphs or title not in undirected_graphs):
    revisions = get_article_revisions(title)
    directed_graphs[title] = create_article_trajectory_graph(revisions, directed=True, weighted=True)
    # undirected_graphs[title] = create_article_trajectory_graph(revisions, directed=False, weighted=True)

with open('./data/directed_network_dictionary.pkl', 'wb') as f:
   pickle.dump(directed_graphs, f)

# with open('./data/undirected_network_dictionary.pkl', 'wb') as f:
#    pickle.dump(undirected_graphs, f)
