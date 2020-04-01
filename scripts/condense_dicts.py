import pickle

classes = ('FA', 'GA', 'B', 'C', 'ST', 'SB')
types = ('graph', 'revision')

for type in types:
    full_dict = {}
    for cl in classes:
        with open('./data/{}_dictionary_{}.pkl'.format(type, cl), 'rb') as f:
             full_dict.update(pickle.load(f))

    with open('./data/{}_dictionary_all.pkl'.format(type), 'wb') as f:
       pickle.dump(full_dict, f)
