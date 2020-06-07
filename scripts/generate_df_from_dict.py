# -*- coding: utf-8 -*-
"""Generate DF from Dictionary

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cZWQ6Aia2rB4NWmGLG8gl32B4VW1bvMd
"""

import networkx as nx
import requests
import json
import matplotlib.pyplot as plt
import statistics

from operator import itemgetter
import pandas as pd
import pickle
import math

""" Original Network Stats """

def get_eccentricities(g, weighted=False):
  w = None
  if (weighted):
    w = "length"
  dicts = [x[1] for x in list(nx.algorithms.shortest_paths.weighted.all_pairs_dijkstra_path_length(g,weight=w))]
  return [max(d.values()) for d in dicts]

def diameter(g, weighted=False):
  if (not weighted):
    return nx.algorithms.distance_measures.diameter(g)
  w = "length"
  dicts = [x[1] for x in list(nx.algorithms.shortest_paths.weighted.all_pairs_dijkstra_path_length(g,weight=w))]
  return max([max(d.values()) for d in dicts])

def average_closeness(g, weighted=False):
  w = None
  if (weighted):
    w = "length"
  return statistics.mean(nx.algorithms.centrality.closeness_centrality(g, distance=w).values())

def average_clustering(g, weighted=False):
  w = None
  if (weighted):
    w = "strength"
  return statistics.mean(nx.algorithms.cluster.clustering(g, weight=w).values())

def average_betweenness(g, weighted=False):
  w = None
  if (weighted):
    w = "length"
  return statistics.mean(nx.networkx.algorithms.centrality.betweenness_centrality(g, weight=w).values())

def unexpected_betweenness(g, aggregator='median'):
  # for G in G_list:
  degree_dict = dict(g.degree(g.nodes()))
  sorted_degree = sorted(degree_dict.items(), key=itemgetter(1), reverse=True)
  top_degree = [a[0] for a in sorted_degree[:max(5, int(len(sorted_degree)/50))]]
  nx.set_node_attributes(g, degree_dict, 'degree')

  betweenness_dict = nx.betweenness_centrality(g) # Run betweenness centrality
  #eigenvector_dict = nx.eigenvector_centrality(G) # Run eigenvector centrality
  # Assign each to an attribute in the network
  nx.set_node_attributes(g, betweenness_dict, 'betweenness')
  # nx.set_node_attributes(G, eigenvector_dict, 'eigenvector')
  # First get the top 20 nodes by betweenness as a list
  sorted_betweenness = sorted(betweenness_dict.items(), key=itemgetter(1), reverse=True)
  top_betweenness = sorted_betweenness[:max(5, int(len(sorted_betweenness)/50))]

  brokers = []
  # Then find and print their degree
  for tb in top_betweenness: # Loop through top_betweenness
    degree = degree_dict[tb[0]] # Use degree_dict to access a node's degree
    if tb[0] not in top_degree:
      print("Name:", tb[0], "| Betweenness Centrality:", tb[1], "| Degree:", degree)
      brokers.append((tb[1], degree))
  
  # if not brokers:

  if aggregator == "median":
    return statistics.median([elm[0] for elm in brokers]) if brokers else 0
  elif aggregator == "mean":
    return statistics.mean([elm[0] for elm in brokers]) if brokers else 0
  elif aggregator == "exp":
    return statistics.mean([elm[0] ** elm[1] for elm in brokers]) if brokers else 0
  return brokers

""" Network Stats 2 """
density = nx.classes.function.density

def radius(g, weighted=False):
  if (not weighted):
    return nx.algorithms.distance_measures.radius(g)
  return min(get_eccentricities(g, weighted=True))

def average_eccentricity(g, weighted=False):
  if (not weighted):
    return statistics.mean( nx.algorithms.distance_measures.eccentricity(g).values() )
  return statistics.mean(get_eccentricities(g, weighted=True))

def number_of_edges(input_graph):
  if (weighted):
    total = 0
    for u, v, count in list(input_graph.edges.data("count")):
      total += count
    return total

  return len(input_graph.edges)

global_clustering = nx.algorithms.cluster.transitivity


""" Network Stats 3 """
# the following 3 stats do not accept weights or directed graphs

def smallworld_omega(g):
  return nx.algorithms.smallworld.omega(g.to_undirected())

def smallworld_sigma(g):
  return nx.algorithms.smallworld.sigma(g.to_undirected())

node_connectivity = nx.algorithms.connectivity.connectivity.node_connectivity

# this stat admits directed graphs but not edge weights
edge_connectivity = nx.algorithms.connectivity.connectivity.edge_connectivity

"""# Data Frame Construction"""

def get_log_weighted_graph(input_graph, directed=True):
  if (directed):
    g = nx.DiGraph()
    for u, v, count in list(input_graph.edges.data("count")):
      g.add_edge(u, v, strength= math.log2(1+count), length= (1/(math.log2(1+count))) )

  else:
    g = nx.Graph()
    for u, v, count in list(input_graph.edges.data("count")):
      transpose_count = input_graph[v][u]["count"]
      g.add_edge(u, v, strength= math.log2(1+ count + transpose_count), length= (1/(math.log2(1+ count + transpose_count))) )

  return g

def get_n_weighted_graph(input_graph, directed=True):
   if (directed):
     g = nx.DiGraph()
     for u, v, count in list(input_graph.edges.data("count")):
       g.add_edge(u, v, strength= count, length= 1/count )

   else:
     g = nx.Graph()
     for u, v, count in list(input_graph.edges.data("count")):
       transpose_count = input_graph[v][u]["count"]
       g.add_edge(u, v, strength= count + transpose_count, length= 1/ (count + transpose_count) )

   return g

def get_sqrtn_weighted_graph(input_graph, directed=True):
  if (directed):
    g = nx.DiGraph()
    for u, v, count in list(input_graph.edges.data("count")):
      g.add_edge(u, v, strength= count**(1/2), length= (1/count**(1/2)) )

  else:
    g = nx.Graph()
    for u, v, count in list(input_graph.edges.data("count")):
      transpose_count = input_graph[v][u]["count"]
      g.add_edge(u, v, strength= (count + transpose_count)**(1/2), length= (1/(count + transpose_count)**(1/2)) )

  return g

stat_functions = {
  'diameter': diameter,
  'closeness' : average_closeness,
  'avg clustering' : average_clustering,
  'betweenness' : average_betweenness,
  'density' : density,
  'radius' : radius,
  'avg eccentricity' : average_eccentricity,
  'm' : number_of_edges,
  'global clustering' : global_clustering,
  'unexpected betweenness' : unexpected_betweenness,
  'smallworld omega': smallworld_omega,
  'smallworld sigma': smallworld_sigma,
  'node connectivity': node_connectivity,
  'edge connectivity': edge_connectivity
}

# cannot do anything that requires the revision history
def create_article_row(index, stat_names, directed, weighted):
  title = titles[index]
  print(index, title)

  graph = graph_dict[title]
  if not directed:
    graph = graph.to_undirected()
  if (weighted == 'log'):
    graph = get_log_weighted_graph(graph, directed=directed)
  if (weighted == 'n'):
    graph = get_n_weighted_graph(graph, directed=directed)
  if (weighted == 'sqrt'):
    graph = get_sqrtn_weighted_graph(graph, directed=directed)

  return (title, *(stat_functions[stat](graph) for stat in stat_names))

def construct_dataframe(article_titles, stat_names, directed, weighted):
  return pd.DataFrame(
    [create_article_row(i, stat_names, directed, weighted) for i in range(len(article_titles))],
    columns = ['title', *stat_names] ).set_index('title')

""" Main Method Section """
   
with open('../../../shared/data/graph_dictionary_all.pkl', 'rb') as f:
 graph_dict = pickle.load(f)

with open('../../../shared/data/article_titles_all.pkl', 'rb') as f:
 class_lists = pickle.load(f)

stats1 = ['diameter', 'closeness', 'avg clustering', 'betweenness']
stats2 = ['density', 'radius', 'avg eccentricity', 'm', 'global clustering', 'unexpected betweennness']
stats_smallworld = ['smallworld omega', 'smallworld sigma']
stats_connectivity = ['node connectivity', 'edge connectivity']
weighted_stats1 = ['diameter', 'closeness', 'avg clustering', 'betweenness', 'radius', 'avg eccentricity']

titles = [item for sublist in class_lists for item in sublist]
directed = False
weighted = ["log", "n", "sqrt"]

df = construct_dataframe(titles, ['unexpected betweenness'], directed, False)

# for weight in weighted:
#   df = construct_dataframe(titles, weighted_stats1, directed, weight)
#   with open('../data/df_{}_weighted_stats_.pkl'.format(weight), 'wb') as f:
#     pickle.dump(df, f)
