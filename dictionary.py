import itertools

with open('dictionary.txt', "r") as file_object:
    # read file content
    data = file_object.read()
    dictionary = data.split("\n")
    dictionary = [d for d in dictionary if len(d) > 2]

def search_dictionary(letters, three_letters=True):
    perms = permutations(letters)
    sub_dict = [word for word in dictionary if word[0] in letters and word[1] in letters and word[2] in letters]
    words = [p for p in perms if p in sub_dict]
    if not three_letters:
        words = [w for w in words if len(w) > 3]
    return words

def permutations(letters):
    perms = []
    for L in range(3, len(letters)+1):
        for subset in itertools.permutations(letters, L):
            perms.append("".join(subset))
    return list(set(perms))