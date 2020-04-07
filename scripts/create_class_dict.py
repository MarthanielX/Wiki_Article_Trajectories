import pickle 

with open('../data/article_titles_all.pkl', 'rb') as f:
  class_lists = pickle.load(f)

class_dict = {}
classes = ('FA', 'GA', 'B', 'C', 'ST', 'SB')
for i in range(len(classes)):
    for title in class_lists[i]:
        class_dict[title] = classes[i]

with open('../data/class_dictionary.pkl', 'wb') as f:
    pickle.dump(class_dict, f)
