import pandas as pd
import pickle
import math

def get_edit_count_list(title):
    hist = revision_dict[title]
    counts = {}

    for i in range(len(revisions)):
        if revisions[i]['user'] in counts:
            counts[ revisions[i]['user'] ] = counts[ revisions[i]['user'] ] + 1
        else:
            counts[ revisions[i]['user'] = 1


    lst = list(counts.values())
    lst.sort(reverse=True)
    return  lst

def construct_row(title):

    ["T5 Avg Count", "T10 Avg Count", "T5% Avg Count", "T10% Avg Count", "Count>5", "Count>10"]
    counts = get_edit_count_list(title)
    lst = []

    lst.append( statistics.mean(counts[:min(n, 5)]))
    lst.append( statistics.mean(counts[:min(n, 10)]))

    lst.append( statistics.mean(counts[: max(n//20, 1) ]))
    lst.append( statistics.mean(counts[: max(n//10, 1) ]))

    lst.append( count([x for x in lst if x >= 5]) )
    lst.append( count([x for x in lst if x >= 10]) )

    return lst

def construct_dataframe(titles):

    cols = ["T5 Avg Count", "T10 Avg Count", "T5% Avg Count", "T10% Avg Count", "Count>5", "Count>10"]
    row_lst = []
    for i, title in enumerate(titles):
        print(i, title)
        row_lst.append(construct_row(title))

    return pd.DataFrame(row_lst, columns = ['title', *cols] ).set_index('title')


with open('../data/article_titles_all.pkl', 'rb') as f:
    titles = pickle.load(f)
titles = [item for sublist in class_lists for item in sublist]

with open('../data/revision_dictionary_all.pkl', 'rb') as f:
    revision_dict = pickle.load(f)

df = construct_dataframe(titles)

with open('../data/df_edit_count_stats.pkl', 'wb') as f:
    pickle.dump(df, f)
