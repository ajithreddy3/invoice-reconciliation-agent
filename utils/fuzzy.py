from rapidfuzz import fuzz

def similarity(a, b):
    return fuzz.token_sort_ratio(a, b) / 100
