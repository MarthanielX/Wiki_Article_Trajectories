import pandas as pd
import pickle
import math
import statistics

def get_edit_count_list(title):
    revisions = revision_dict[title]
    counts = {}

    for i in range(len(revisions)):
        if revisions[i]['user'] in counts:
            counts[ revisions[i]['user'] ] = counts[ revisions[i]['user'] ] + 1
        else:
            counts[ revisions[i]['user'] ] = 1


    lst = list(counts.values())
    lst.sort(reverse=True)
    return  lst

def construct_row(title):

    #["T8 Avg Count", "T12 Avg Count", "T15 Avg Count", "Count>2", "Count>4", "Count>7"]
    counts = get_edit_count_list(title)
    lst = [title,]

    n = len(counts)

    for i in range(1, 16):
        lst.append( statistics.mean(counts[:min(n, i)]))

    #lst.append( statistics.mean(counts[:min(n, 12)]))
    #lst.append( statistics.mean(counts[:min(n, 15)]))

    #lst.append( statistics.mean(counts[: max(n//20, 1) ]))
    #lst.append( statistics.mean(counts[: max(n//10, 1) ]))

    for i in range(2, 16):
        lst.append( len([x for x in counts if x >= i]) )
    
    #lst.append( len([x for x in counts if x >= 4]) )
    #lst.append( len([x for x in counts if x >= 7]) )

    return lst

def construct_dataframe(titles):

    #cols = ["T5 Avg Count", "T10 Avg Count", "T5% Avg Count", "T10% Avg Count", "Count>5", "Count>10"]
    #cols = ["T8 Avg Count", "T12 Avg Count", "T15 Avg Count", "Count>2", "Count>4", "Count>7"]
    cols = ["T{} Avg Count".format(i) for i in range(1, 16)] + ["Count>i".format(i) for i in range(2, 16)]
    
    row_lst = []
    for i, title in enumerate(titles):
        print(i, title)
        row_lst.append(construct_row(title))

    return pd.DataFrame(row_lst, columns = ['title', *cols] ).set_index('title')


with open('../data/article_titles_all.pkl', 'rb') as f:
    class_lists  = pickle.load(f)
titles = [item for sublist in class_lists for item in sublist]

with open('../data/revision_dictionary_all.pkl', 'rb') as f:
    revision_dict = pickle.load(f)

df = construct_dataframe(titles)

with open('../data/df_edit_count_stats2.pkl', 'wb') as f:
    pickle.dump(df, f)
