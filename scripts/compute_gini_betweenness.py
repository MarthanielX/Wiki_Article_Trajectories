import pandas as pd
import pickle
import math
import statistics

def construct_row(title):

  title = article_titles[i]
  graph = graph_dict[title]
  print(i, title)
  return (
    title,
    gini(betweenness_list(graph))
  )

def construct_dataframe(article_titles):
  rows = [create_article_row(i) for i in range(len(article_titles))]
  return pd.DataFrame(rows, columns = ['title', 'gini betweenness']).set_index('title')

def betweenness_list(g):
  return nx.networkx.algorithms.centrality.betweenness_centrality(g).values()

def gini(data):
    '''
    Calculates the gini coefficient for a given dataset.
    input:
        data- list of values, either raw counts or frequencies.
              Frequencies MUST sum to 1.0, otherwise will be transformed to frequencies
              If raw counts data will be transformed to frequencies.
    output:
        gini- float, from 0.0 to 1.0 (1.0 most likely never realized since it is
              only achieved in the limit)
    '''

    def _unit_area(height, value, width):
        '''
        Calculates a single bars area.
        Area is composed of two parts:
            The height of the bar up until that point
            The addition from the current value (calculated as a triangle)
        input:
            height: previous bar height or sum of values up to current value
            value: current value
            width: width of individual bar
        output:
            bar_area: area of current bar
        '''
        bar_area = (height * width) + ((value * width) / 2.)
        return bar_area

    #Fair area will always be 0.5 when frequencies are used
    fair_area = 0.5
    #Check that input data has non-zero values, if not throw an error
    datasum = float(sum(data))
    if datasum==0:
        import sys
        m = 'Data sum is 0.0.\nCannot calculate Gini coefficient for non-responsive population.'
        print(m)
        sys.exit()
    #If data does not sum to 1.0 transform to frequencies
    if datasum!=1.0:
        data = [x/datasum for x in data]
    #Calculate the area under the curve for the current dataset
    data.sort()
    width = 1/float(len(data))
    height, area = 0.0, 0.0
    for value in data:
        area += _unit_area(height, value, width)
        height += value
    #Calculate the gini
    gini = (fair_area-area)/fair_area
    return gini

#with open('../../../shared/data/article_titles_all.pkl', 'rb') as f:
with open('../data/article_titles_all.pkl', 'rb') as f:
    class_lists  = pickle.load(f)
titles = [item for sublist in class_lists for item in sublist]

#with open('../../../shared/data/revision_dictionary_all.pkl', 'rb') as f:
with open('../data/revision_dictionary_all.pkl', 'rb') as f:
    revision_dict = pickle.load(f)

df = construct_dataframe(titles)

with open('../data/df_gini_betweenness.pkl', 'wb') as f:
    pickle.dump(df, f)
