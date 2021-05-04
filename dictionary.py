import itertools
from random import shuffle

with open('dictionary.txt', "r") as file_object:
    # read file content
    blob = file_object.read()
    dictionary = blob.split("\n")
    dictionary = [d.upper() for d in dictionary if len(d) > 2]

with open('dictionary2.txt', "r") as file_object:
    # read file content
    dictionary2 = file_object.read()
    dictionary2 = dictionary2.split("\n")
    dictionary2 = [d.upper().strip() for d in dictionary2 if len(d) > 2 and len(d) < 9]

# with open('dictionary3.txt', "r") as file_object:
#     # read file content
#     data3 = file_object.read()
#     dictionary3 = data3.split("\n")
#     dictionary3 = [d.upper().strip() for d in dictionary3 if len(d) > 2 and len(d) < 9]

# dictionary3 = [x for x in dictionary3 if x not in dictionary]
# dictionary2 = list(set(dictionary2 + dictionary3))
# dictionary2.sort()

# with open('dictionary4.txt', "w") as file_object:
#     file_object.write("\n".join(dictionary2))


dictionary = [d.upper().strip() for d in dictionary]
dictionary = [d for d in dictionary if "'" not in d]
dictionary = [d for d in dictionary if len(d) > 2 and len(d) < 9]
dictionary.sort()



def search_backup_dictionary(letters, three_letters=True):
    perms = permutations(letters)
    sub_dict = [word for word in dictionary2 if word[0] in letters and word[1] in letters and word[2] in letters]
    words = [p for p in perms if p in sub_dict]
    if not three_letters:
        words = [w for w in words if len(w) > 3]
    words.sort(key=len)
    return words

def search_dictionary(letters, three_letters=True):
    perms = permutations(letters)
    sub_dict = [word for word in dictionary if word[0] in letters and word[1] in letters and word[2] in letters]
    words = [p for p in perms if p in sub_dict]
    if not three_letters:
        words = [w for w in words if len(w) > 3]
    words.sort(key=len)
    return words

def permutations(letters):
    perms = []
    for L in range(3, len(letters)+1):
        for subset in itertools.permutations(letters, L):
            perms.append("".join(subset))
    return list(set(perms))


def sort_words_20x(words, max_length):
    longest_words = [w for w in words if len(w) == max_length]
    words = [w for w in words if len(w) != max_length]
    best_score = 0
    best_list = words
    for i in range(50):
        shuffle(words)
        sorted_words = sort_words(words)+longest_words
        score = score_list(sorted_words)
        if score > best_score:
            best_score = score
            best_list = sorted_words
    return best_list

def score_list(words):
    count = 0
    for word, next_word in zip(words, words[1:]):
        if word[-1] == next_word[0]:
            count += 1
    return count

def brute_force(letters, template):
    template = template.upper().strip()
    listed_words = search_dictionary(letters)+search_backup_dictionary(letters)
    paths = permutations(letters)
    paths = [p for p in paths if len(p) == len(template)]
    paths = [p for p in paths if p not in listed_words]
    for i, letter in enumerate(template):
        if letter == "_": continue
        if letter == "*": continue
        paths = [p for p in paths if letter == p[i]]

    unvalid_paths = []
    likely_paths = []
    for path in paths:
        for i in range(0, len(template)-2):
            if path[i:i+3] not in blob:
                unvalid_paths.append(path)
                break
        else:
            if path in blob:
                likely_paths.append(path)

    valid_paths = [p for p in paths if path not in unvalid_paths]
    valid_paths = [p for p in paths if path not in likely_paths]

    return sort_words(likely_paths)+sort_words(valid_paths)


def sort_words(words):
    words = words[:]
    word = words[0]
    new_list = [word]
    words.remove(word)
    while words:
        elem = new_list[-1]
        for word in words:
            if elem[-1] == word[0]:
                words.remove(word)
                new_list.append(word)
                break
        else:
            word = words[0]
            words.remove(word)
            new_list.append(word)
    return new_list

#words = brute_force("ILGNOB", "*****")
#print(words)
