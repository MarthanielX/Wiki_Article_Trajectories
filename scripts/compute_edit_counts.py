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

def get_edit_size_list(title, variant='default'):
    revisions = revision_dict[title]
    sizes = {revisions[-1]['user']: revisions[-1]['size']}

    for i in range(len(revisions[:-1])):
        edit_size = revisions[i]['size'] - revisions[i+1]['size']
        if revisions[i]['user'] in sizes:
            if variant == 'default':
                sizes[ revisions[i]['user'] ] += edit_size
            if variant == 'added':
                sizes[ revisions[i]['user'] ] += edit_size if edit_size > 0 else 0
            if variant == 'removed':
                sizes[ revisions[i]['user'] ] += edit_size if edit_size < 0 else 0
        else:
            if variant == 'default':
                sizes[ revisions[i]['user'] ] = edit_size
            if variant == 'added':
                sizes[ revisions[i]['user'] ] = edit_size if edit_size > 0 else 0
            if variant == 'removed':
                sizes[ revisions[i]['user'] ] = edit_size if edit_size < 0 else 0

    lst = list(sizes.values())
    lst.sort(reverse=True)

    return lst

def construct_row(title):

    #["T8 Avg Count", "T12 Avg Count", "T15 Avg Count", "Count>2", "Count>4", "Count>7"]
    
    # counts = get_edit_count_list(title)
    # lst = [title,]

    sizes = get_edit_size_list(title)
    lst = [title,]

    # n = len(counts)
    n = len(sizes)

    for i in range(1, 16):
        # lst.append( statistics.mean(counts[:min(n, i)]))
        lst.append( statistics.mean(sizes[:min(n, i)]))

    #lst.append( statistics.mean(counts[:min(n, 12)]))
    #lst.append( statistics.mean(counts[:min(n, 15)]))

    #lst.append( statistics.mean(counts[: max(n//20, 1) ]))
    #lst.append( statistics.mean(counts[: max(n//10, 1) ]))

    # for i in range(2, 16):
        # lst.append( len([x for x in counts if x >= i]) )
        # lst.append( len([x for x in sizes if x >= i]) )
    
    #lst.append( len([x for x in counts if x >= 4]) )
    #lst.append( len([x for x in counts if x >= 7]) )

    return lst

def construct_dataframe(titles):

    #cols = ["T5 Avg Count", "T10 Avg Count", "T5% Avg Count", "T10% Avg Count", "Count>5", "Count>10"]
    #cols = ["T8 Avg Count", "T12 Avg Count", "T15 Avg Count", "Count>2", "Count>4", "Count>7"]
    # cols = ["T{} Avg Count".format(i) for i in range(1, 16)] + ["Count>i".format(i) for i in range(2, 16)]
    cols = ["T{} Avg Edit Size".format(i) for i in range(1, 16)] #+ ["Edit Size>i".format(i) for i in range(2, 16)]
    
    row_lst = []
    for i, title in enumerate(titles):
        print(i, title)
        row_lst.append(construct_row(title))

    return pd.DataFrame(row_lst, columns = ['title', *cols] ).set_index('title')


with open('../../../shared/data/article_titles_all.pkl', 'rb') as f:
#with open('../data/article_titles_all.pkl', 'rb') as f:
    class_lists  = pickle.load(f)
titles = [item for sublist in class_lists for item in sublist]

with open('../../../shared/data/revision_dictionary_all.pkl', 'rb') as f:
#with open('../data/revision_dictionary_all.pkl', 'rb') as f:
    revision_dict = pickle.load(f)

df = construct_dataframe(titles)

with open('../data/df_edit_size_stats.pkl', 'wb') as f:
    pickle.dump(df, f)
