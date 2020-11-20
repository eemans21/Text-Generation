  import utilities 

VALID_PUNCTUATION = ['?', '.' , '!', ',', ':', ';']
END_OF_SENTENCE_PUNCTUATION = ['?', '.', '!']
ALWAYS_CAPITALIZE = ["I", "Montmorency", "George", "Harris", "J", "London", "Thames", "Liverpool", \
                     "Flatland", "", "Mrs", "Ms", "Mr", "William", "Samuel"]
BAD_CHARS = ['"', "(", ")", "{", "}", "[", "]", "_"]

def parse_story(file_name):  

    """  

    (list) --> list 

    This function takes a text file and returns a list in which all the bad
    characters defined in BAD_CHARS are removed.

    Example: 

    >>parse_story('test_text_parsing.txt')  

    ['the', 'code', 'should', 'handle', 'correctly', 'the', 'following', ':', 'white', 'space', '.', 'sequences', 'of', 'punctuation', 'marks', '?', '!', '!', 'periods', 'with', 'or', 'without', 'spaces', ':', 'a', '.', '.', 'a', '.', 'a', "don't", 'worry', 'about', 'numbers', 'like', '1', '.', '5', 'remove', 'capitalization']

    """

    ordered_list = []
    word = ""

    file = open(file_name, "a")
    file.write(" ")
    file.close()

    file = open(file_name, "r")
    line = file.readline()

    while line != "":

        for character in line: 

            ascii_value = ord(character)

            #is the character a lowerecase letter or an apostrophe? 
            if (ascii_value == 39) or (ascii_value >= 97 and ascii_value <= 122):
                #yes, so add to word
                word = word + character

            #is the character a capital letter? 
            elif (ascii_value <= 90 and ascii_value >= 65): 

                #yes, so change to lowercase and add to word
                word = word + chr(ascii_value + 32)

            else: 
                #add word to list
                if word != "": 
                    ordered_list.append(word)
                word = ""

            #is the character a number or valid punctuation? 
            if (ascii_value <= 59 and ascii_value >= 48) or (ascii_value == 63 or ascii_value == 46 or ascii_value == 33 or ascii_value == 44): 

                #yes, so add to list
                ordered_list.append(character)

        line = file.readline()

    file.close()
    return ordered_list

def get_prob_from_count(count):

    """
    (list) --> list

    This function takes a list of the number of occurances of a token from the previous n_gram and returns a list of the derived probablities.

    Example: 

    >>>get_prob_from_count([10, 20, 40, 30])
    [0.1, 0.2, 0.4, 0.3]
    """

    sum = 0
    probability = 0
    probabilities = []

    for occurance in count: 
        sum += occurance

    for occurance in count: 
        probability = occurance / sum
        probabilities.append(probability)

    return probabilities


def build_ngram_counts(words, n): 
    """

    (list, int) --> dict

    This function takes a list of words obtained from the parse_story function and the size of the N-gram and returns a dictionary with N-grams as the key with corresponding values that contain the counts of the words that follow the n-gram. 

    Example: 
    
    >>>build_ngram_counts([‘the’, ‘child’, ‘will’, ‘go’, ‘out’, ‘to’, ‘play’, ‘,’, ‘and’, ‘the’, ‘child’, ‘can’, ‘not’, ‘be’, ‘sad’, ‘anymore’,‘.’], 2)

    {
        (‘the’, ‘child’): [[‘will’, ‘can’], [1, 1]],
        (‘child’, ‘will’): [[‘go’], [1]],
        (‘will’, ‘go’): [[‘out’], [1]],
        (‘go’, out’): [[‘to’], [1]],
        (‘out’, ‘to’): [[‘play’], [1]],
        (‘to’, ‘play’): [[‘,’], [1]],
        (‘play’, ‘,’): [[‘and’], [1]],
        (‘,’, ‘and’): [[‘the’], [1]],
        (‘and’, ‘the’): [[‘child’], [1]],
        (‘child’, ‘can’): [[‘not’], [1]],
        (‘can’, ‘not’): [[‘be’], [1]],
        (‘not’, ‘be’): [[‘sad’], [1]],
        (‘be’, ‘sad’): [[‘anymore’], [1]],
        (‘sad’, ‘anymore’): [[‘.’], [1]]
    }

    """

    number_of_words = len(words)
    lastword = []
    dictionary = {}
    list_of_tuples = []

    for item in range(number_of_words):
        temp = ()

        if item < (number_of_words - (n - 1) - 1):
            for i in range(n): 
                temp += (words[item + i],)

                if i == n-1:
                    lastword.append(words[item + i + 1])


        if temp != (): 
            list_of_tuples.append(temp)

    for item in range(len(list_of_tuples)):
        newList = []
        count = []
        if list_of_tuples[item] not in dictionary.keys(): 

            newList = [[lastword[item]], [1]]
            dictionary[list_of_tuples[item]] = newList

        else: 
            index = list_of_tuples.index(list_of_tuples[item])

            indices = [i for i, x in enumerate(list_of_tuples) if x == list_of_tuples[item]]
            for i in indices: 
                newList.append(lastword[i])

            for word in newList: 
                if newList.count(word) > 1: 
                    count.append(newList.count(word))
                    for sameword in range(newList.count(word) - 1):
                        newList.reverse()
                        newList.remove(word)
                        newList.reverse()
                else: 
                    count.append(1)

            dictionary.update({list_of_tuples[index] : [newList, count]})

    return dictionary

#build_ngram_counts(['the', 'child', 'will', 'go', 'out', 'to', 'play', ',', 'and', 'the', 'child', 'can', 'not', 'be', 'sad', 'anymore','.'], 2)

#build_ngram_counts(['the', 'child', 'will', 'the', 'child', 'can', 'the', 'child', 'will', 'the', 'child', 'may', 'go', 'home', '.'], 2)

def prune_ngram_counts(counts, prune_len):
    """
    (dict, int) --> dict

    This function takes a dictionary of which the keys are n-grams and the values are the words that follow the n-gram and their respective counts (result from build_ngram_counts), and the number of highest frequency words to keep. It returns a dictionary with the same keys, but the values contain only the words with high frequencies. 

    Example: 

    >>>ngram_counts = {(‘i’, ‘love’): [[‘js’, ‘py3’, ‘c’, ‘no’], [20, 20, 10, 2]], (‘u’, ‘r’): [[‘cool’, ‘nice’, ‘lit’, 'kind’], [8, 7, 5, 5]], ('toronto’, ‘is’): [[‘six’, ‘drake’], [2, 3]]}

    >>>prune_ngram_counts(ngram_counts, 3)

    {(‘i’, ‘love’): [[‘js’, ‘py3’, ‘c’], [20, 20, 10]], (‘u’, ‘r’): [[‘cool’, ‘nice’, ‘lit’, 'kind’], [8, 7, 5, 5]], ('toronto’, ‘is’): [[‘six’, ‘drake’], [2, 3]]}
    """

    finalWords = []
    finalCounts = []

    for key, value in counts.items(): 

        countCopy = value[1].copy()
        countCopy.sort()
        countCopy.reverse()

        if len(value[1]) >= prune_len: 

            for count in countCopy:

                if len(finalCounts) < prune_len: 
                    finalCounts.append(count)
                else: 
                    if count in finalCounts: 
                        finalCounts.append(count)
                    elif count > min(finalCounts): 
                        finalCounts.replace(finalCounts.index(min(finalCounts)), count)

            for count in finalCounts: 

                if finalCounts.count(count) > 1: 
                    indices= [i for i, x in enumerate(value[1]) if x == count]

                    for index in indices: 
                        finalWords.append(value[0][index])

                else: 
                    finalWords.append(value[0][value[1].index(count)])
            
            finalWords = list(dict.fromkeys(finalWords))

            counts.update({key : [finalWords, finalCounts]})
            finalWords = []
            finalCounts = []

    return counts


#ngram_counts = {('i', 'love'): [['js', 'py3', 'c', 'no'], [20, 20, 10, 2]], ('u', 'r'): [['cool', 'nice', 'lit', 'kind'], [8, 7, 5, 5]], ('toronto', 'is'): [['six', 'drake'], [2, 3]]}

#prune_ngram_counts(ngram_counts, 2)

def probify_ngram_counts(counts): 
    """
    (dict) --> dict

    This function takes a dictionary with N-grams as keys and a nested list of words and counts as the values. The function converts the counts into probabilities, and returns a dictionary with probabilities as the valuesn instead.  

    Example: 

    >>> ngram_counts = {(‘i’, ‘love’): [[‘js’, ‘py3’, ‘c’], [20, 20, 10]], (‘u’, ‘r’): [[‘cool’, ‘nice’, ‘lit’, 'kind’], [8, 7, 5, 5]], ('toronto’, ‘is’): [[‘six’, ‘drake’], [2, 3]]}

    >>> probify_ngram_counts(ngram_counts)
    {(‘i’, ‘love’): [[‘js’, ‘py3’, ‘c’], [0.4, 0.4, 0.2]], (‘u’, ‘r’): [[‘cool’, ‘nice’, ‘lit’, 'kind’], [0.32, 0.28, 0.2, 0.2]], ('toronto’, ‘is’): [[‘six’, ‘drake’], [0.4, 0.6]]}

    """


    for key, value in counts.items(): 

        probabilities = get_prob_from_count(value[1])

        counts.update({key : [value[0], probabilities]})

    return counts

#ngram_counts = {('i', 'love'): [['js', 'py3', 'c'], [20, 20, 10]], ('u', 'r'): [['cool', 'nice', 'lit', 'kind'], [8, 7, 5, 5]], ('toronto', 'is'): [['six', 'drake'], [2, 3]]}

#probify_ngram_counts(ngram_counts)


def build_ngram_model(words, n):
    """

    (list, int) --> dict

    This function takes a list of words and punctuation and the size of the N-gram desired. It returns a dictionary with N-grams of size n as keys, and a nested list of corresponding next words and probabilities as values. The corresponding next words in the returned dictionary appear in descending order of probability. 

    Example: 

    >>> words = [‘the’, ‘child’, ‘will’, ‘the’, ‘child’, ‘can’, ‘the’, ‘child’, ‘will’, ‘the’, ‘child’, ‘may’, ‘go’, ‘home’, ‘.’]

    >>> build_ngram_model(words, 2)
    { 
        (‘the’, ‘child’): [[‘will’, ‘can’, ‘may’], [0.5, 0.25, 0.25]],
        (‘child’, ‘will’): [[‘the’], [1.0]],
        (‘will’, ‘the’): [[‘child’], [1.0]],
        (‘child’, ‘can’): [[‘the’], [1.0]],
        (‘can’, ‘the’): [[‘child’], [1.0]],
        (‘child’, ‘may’): [[‘go’], [1.0]],
        (‘may’, ‘go’): [[‘home’], [1.0]],
        (‘go’, ‘home’): [[‘.’], [1.0]]
    }
    
    """

    counts = probify_ngram_counts(build_ngram_counts(words, n))

    newWords = []

    for key, value in counts.items(): 

        probabilitiesCopy = value[1].copy()
        probabilitiesCopy.sort()
        probabilitiesCopy.reverse()

        for probability in probabilitiesCopy: 
            if probabilitiesCopy.count(probability) > 1: 

                indices= [i for i, x in enumerate(value[1]) if x == probability]

                for index in indices: 
                    newWords.append(value[0][index])

            else: 
                newWords.append(value[0][value[1].index(probability)])
            
        newWords = list(dict.fromkeys(newWords))

        counts.update({key : [newWords, probabilitiesCopy]})
        newWords = []

    return counts


#words = ['the', 'child', 'will', 'the', 'child', 'can', 'the', 'child', 'will', 'the', 'child', 'may', 'go', 'home', '.']
#build_ngram_model(words, 2)
