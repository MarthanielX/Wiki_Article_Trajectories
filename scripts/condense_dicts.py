import pickle

classes = ('FA', 'GA', 'B', 'C', 'ST', 'SB')
types = ('graph', 'revision')

for type in types:
    dicts = []
    for class in classes:
        with open('./data/{}_dictionary_{}.pkl'.format(type, class), 'rb') as f:
             dicts.append(pickle.load(f))

    full_dict = {**x for x in dicts}

    with open('./data/{}_dictionary_all.pkl'.format(type), 'wb') as f:
       pickle.dump(full_dict, f)
