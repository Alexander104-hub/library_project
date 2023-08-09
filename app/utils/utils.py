import itertools

NWORDS_IN_COMBINATION = 3

def get_word_combinations(sentence:list[str], nwords_in_combination=NWORDS_IN_COMBINATION):
    word_combinations = []
    for i in range(len(sentence) - nwords_in_combination):
        for L in range(1, nwords_in_combination + 1):
            for subset in itertools.combinations(sentence[i:(i+nwords_in_combination)], L):
                word_combinations.append(subset)
    return word_combinations