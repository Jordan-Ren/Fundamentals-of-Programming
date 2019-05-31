# NO ADDITIONAL IMPORTS!
from text_tokenize import tokenize_sentences


class Trie:
    def __init__(self):
        self.value = None
        self.children = {}
        self.type = None

    def set(self, key, value):
        """
        Add a key with the given value to the trie, or reassign the associated
        value if it is already present in the trie.  Assume that key is an
        immutable ordered sequence.  Raise a TypeError if the given key is of
        the wrong type.
        """
        if self.type == None:
            self.type = type(key)
        if type(key) != self.type:
            raise TypeError
        if len(key) == 0:
            self.value = value
        else:
            if key[0:1] in self.children:
                self.children[key[0:1]].set(key[1:], value)
            else:
                new_t = Trie()
                self.children[key[0:1]] = new_t
                new_t.set(key[1:], value)

    def get(self, key):
        """
        Return the value for the specified prefix.  If the given key is not in
        the trie, raise a KeyError.  If the given key is of the wrong type,
        raise a TypeError.
        """
        if self.type == None:
            self.type = type(key)
        if type(key) != self.type:
            raise TypeError
        if len(key) == 0:
            if self.value is None:
                raise KeyError
            else:
                return self.value
        else:
            if type(key) == tuple:
                if (key[0], ) in self.children:
                    return self.children[(key[0], )].get(key[1:])
                else:
                    raise KeyError
            else:
                if key[0] in self.children:
                    return self.children[key[0]].get(key[1:])
                else:
                    raise KeyError


    def delete(self, key):
        """
        Delete the given key from the trie if it exists.
        """
        self.set(key, None)

    def contains(self, key):
        """
        Is key a key in the trie? return True or False.
        """
        try:
            if self.get(key) != None:
                return True
            else:
                return False
        except KeyError:
            return False

    def items(self):
        """
        Returns a list of (key, value) pairs for all keys/values in this trie and
        its children.
        """
        L = []
        for i in self.children:
            n = i
        if self.type == tuple:
            temp = tuple()
        else:
            temp = ""
        final = self.items_helper(L, temp)
        return final

    def items_helper(self, final, temp):
        if self.children == {} and self.value != None:
            result = final.append((temp, self.value))
            if isinstance(temp, tuple):
                temp = ()
            else:
                temp = ""
                return result
            return result
        else:
            if self.value != None:
                final.append((temp, self.value))
            for root in self.children:
                new_temp = temp + root
                self.children[root].items_helper(final, new_temp)
        return final

def make_word_trie(text):
    """
    Given a piece of text as a single string, create a Trie whose keys are the
    words in the text, and whose values are the number of times the associated
    word appears in the text
    """
    t = Trie()
    key_counts = {}
    new_text = tokenize_sentences(text)
    for sentence in new_text:
        new_s = sentence.split(' ')
        for word in new_s:
            if word in key_counts:
                key_counts[word] += 1
            else:
                key_counts[word] = 1
    for key in key_counts:
        t.set(key, key_counts[key])
    return t

def make_phrase_trie(text):
    """
    Given a piece of text as a single string, create a Trie whose keys are the
    sentences in the text (as tuples of individual words) and whose values are
    the number of times the associated sentence appears in the text.
    """
    t = Trie()
    key_counts = {}
    new_text = tokenize_sentences(text)
    for sentence in new_text:
        new_s = tuple(sentence.split(' '))
        if new_s in key_counts:
            key_counts[new_s] += 1
        else:
            key_counts[new_s] = 1
    for key in key_counts:
        t.set(key, key_counts[key])
    return t

def autocomplete(trie, prefix, max_count=None):
    """
    Return the list of the most-frequently occurring elements that start with
    the given prefix.  Include only the top max_count elements if max_count is
    specified, otherwise return all.

    Raise a TypeError if the given prefix is of an inappropriate type for the
    trie.
    """
    if trie.type != type(prefix):
        raise TypeError
    words = prefix_checker(trie, prefix, max_count)
    if words == []:
        return words
    final = []
    if max_count == None:
        for tup in words:
            final.append(tup[0])
        return final
    for i in range(max_count):
        temp = set()
        for tup in words:
            temp.add(tup[1])
        if temp == set():
            break
        else:
            m = max(temp)
        for tup in words:
            if tup[1] == m:
                final.append(tup[0])
                words.remove(tup)
                temp  = set()
                break
    return final



def prefix_checker(trie, prefix, max_count):
    result = []
    items = trie.items()
    for tup in items:
        if type(tup[0]) == tuple:
            tag = True
            for i in range(len(prefix)):
                if len(tup[0]) >= len(prefix):
                    if prefix[i] != tup[0][i]:
                        tag = False
                else:
                    tag = False
            if tag:
                result.append((tup[0], tup[1]))
        else:
            if tup[0].startswith(prefix):
                result.append((tup[0], tup[1]))
    return result

def autocorrect(trie, prefix, max_count=None):
    """
    Return the list of the most-frequent words that start with prefix or that
    are valid words that differ from prefix by a small edit.  Include up to
    max_count elements from the autocompletion.  If autocompletion produces
    fewer than max_count elements, include the most-frequently-occurring valid
    edits of the given word as well, up to max_count total elements.
    """
    auto_comp = autocomplete(trie,prefix, max_count)
    items = trie.items()
    valid_words = set()
    valid_words = set(tup[0] for tup in items if tup[0] not in auto_comp)
    result = [word for word in auto_comp]
    temp = []
    while max_count != len(auto_comp):
        if len(result) == max_count:
            break
        word_1 = c_insertion(valid_words, prefix)
        word_2 = c_deletion(valid_words, prefix)
        word_3 = c_replacement(valid_words, prefix)
        word_4 = two_c_transpose(valid_words, prefix)
        temp.append(word_1)
        temp.append(word_2)
        temp.append(word_3)
        temp.append(word_4)
        if temp == [[],[],[],[]]:
            break
        new_valid = [tup for tup in items if tup[0] not in auto_comp]
        max_word = max((tup for list in temp
                            if list != []
                            for word in list
                            for tup in new_valid
                            if tup[0] == word), key=lambda x: x[1])[0]
        result.append(max_word)
        valid_words.remove(max_word)
        temp = []
    return result



def c_insertion(valid_words, prefix):
    final = []
    for i in range(97,123):
        char = chr(i)
        for j in range(len(prefix)+1):
            new_prefix = prefix[0:j] + char + prefix[j:len(prefix)]
            if new_prefix in valid_words:
                final.append(new_prefix)
    return final

def c_deletion(valid_words, prefix):
    final = []
    for j in range(len(prefix)):
        new_prefix = prefix[:j] + prefix[j+1:]
        if new_prefix in valid_words:
            final.append(new_prefix)
    return final

def c_replacement(valid_words, prefix):
    final = []
    for i in range(97,123):
        char = chr(i)
        for j in range(len(prefix)):
            new_prefix = prefix[:j] + char + prefix[j+1:]
            if new_prefix in valid_words:
                final.append(new_prefix)
    return final

def two_c_transpose(valid_words, prefix):
    final =[]
    for i in range(len(prefix) -1):
        pre_lst = list(prefix)
        pre_lst[i+1], pre_lst[i] = pre_lst[i], pre_lst[i+1]
        new_prefix =  ''.join(pre_lst)
        if new_prefix in valid_words:
            final.append(new_prefix)
    return final


def word_filter(trie, pattern):
    """
    Return list of (word, freq) for all words in trie that match pattern.
    pattern is a string, interpreted as explained below:
         * matches any sequence of zero or more characters,
         ? matches any single character,
         otherwise char in pattern char must equal char in word.
    """
    final = set()
    temp = ''
    def word_helper(trie, pattern, temp):
        if len(pattern) == 0:
            if trie.value != None:
                final.add((temp, trie.value))
        else:
            if len(pattern) == 1 and pattern == '*' and trie.value != None:
                final.add((temp, trie.value))
            while len(pattern) > 2 and pattern[0] == '*':
                if pattern[1] == '*':
                    pattern = pattern[1:]
                else:
                    break
            if pattern[0] == '*':
                word_helper(trie, pattern[1:], temp)
            # if set(pattern) == {'*'} and trie.value != None:
            #     final.add((temp, trie.value))
            for child in trie.children:
                if child == pattern[0]:
                    temp = temp + child
                    word_helper(trie.children[child], pattern[1:], temp)
                    temp = temp[:-1]
                elif pattern[0]== '?':
                    temp = temp + child
                    word_helper(trie.children[child], pattern[1:], temp)
                    temp = temp[:-1]
                elif pattern[0] == '*':
                    temp = temp + child
                    word_helper(trie.children[child], pattern, temp)
                    word_helper(trie.children[child], pattern[1:], temp)
                    temp = temp[:-1]
    word_helper(trie, pattern, temp)
    result = list(final)
    return result


# you can include test cases of your own in the block below.
if __name__ == '__main__':
    with open("Pride and Prejudice.txt", encoding="utf-8") as f:
        text = f.read()
    tree = make_phrase_trie(text)
    # print(tree.items())
    print(autocomplete(tree, "", 4))
    # print(tree.get('the'))
    # print(tree.get('to'))
    # print(tree.get('and'))
    # print(tree.get('of'))



    pass
