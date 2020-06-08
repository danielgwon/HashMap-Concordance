# word_count.py
# ===================================================
# Implement a word counter that counts the number of
# occurrences of all the words in a file. The word
# counter will return the top X words, as indicated
# by the user.
# ===================================================

import re
from hash_map import HashMap

"""
This is the regular expression used to capture words. It could probably be endlessly
tweaked to catch more words, but this provides a standard we can test against, so don't
modify it for your assignment submission.
"""
rgx = re.compile("(\w[\w']*\w|\w)")

def hash_function_2(key):
    """
    This is a hash function that can be used for the hashmap.
    """

    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash

def top_words(source, number):
    """
    Takes a plain text file and counts the number of occurrences of case insensitive words.
    Returns the top `number` of words in a list of tuples of the form (word, count).

    Args:
        source: the file name containing the text
        number: the number of top results to return (e.g. 5 would return the 5 most common words)
    Returns:
        A list of tuples of the form (word, count), sorted by most common word. (e.g. [("a", 23), ("the", 20), ("it", 10)])
    """

    keys = set()

    ht = HashMap(2500,hash_function_2)

    # This block of code will read a file one word as a time and
    # put the word in `w`. It should be left as starter code.
    with open(source) as f:
        for line in f:
            words = rgx.findall(line)
            for w in words:
                word = w.lower()

                # check if the word is in the hash table
                if word in keys:

                    # if the word is in the hash table, add one to the value of it's node
                    ht.put(word, ht.get(word) + 1)

                # if the word is not in the hash table, add the word to the table with a value of one
                else:
                    keys.add(word)
                    ht.put(word, 1)

    # place all words and counts in an array as tuples
    words_count = [(key, ht.get(key)) for key in keys]

    # sort the words in the hash table by count
    words_count.sort(reverse=True, key=sort_by_value)

    return words_count[:number]

def sort_by_value(tuple):
    """
    Returns the value element of the given tuple
    :param tuple: a tuple with the following elements (key, value)
    :return: value element of tuple
    """
    return tuple[1]


# top_number = 10
# word_values = top_words("alice.txt",top_number)
# for i in range(top_number):
#     print(i+1, word_values[i])