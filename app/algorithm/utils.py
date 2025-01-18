import random
from typing import List, Tuple
from sklearn.decomposition import PCA
import numpy as np 
from app.algorithm.Pair import Pair

def compare_tuples(t1, t2):
    if t1[1] < t2[1]:
        return -1
    elif t1[1] > t2[1]:
        return 1
    else:
        return -1 if t1[0] < t2[0] else 1

def perform_pca(pairs: List[Pair]):
    vectors = list(map(lambda x : x.xs, pairs))
    original = np.vstack(vectors)
    pca = PCA(n_components=3)
    reduced_data = pca.fit_transform(original)
    out = []
    for i in range(len(pairs)):
        index = pairs[i].index
        new_xs = reduced_data[i, :]
        out.append(Pair(index, new_xs))
    return out

def convert_distances(pairs: List[Pair]):
    target = pairs[0]
    f = lambda p : (p.index, np.linalg.norm(target.xs - p.xs))
    return list(map(f, pairs[1:]))

def quick_select(pairs: List[Tuple[int, float]], k):
    quick_select_helper(pairs, 0, len(pairs) - 1, k)
    return pairs[:k]

def quick_select_helper(xs: List[Tuple[int, float]], left, right, k):
    if left < right: 
        index = partition(xs, left, right)
        # print(index)
        
        count = index + 1
        if count == k:
            return
        elif k < index:
            return quick_select_helper(xs, left, index - 1, k)
        else:
            return quick_select_helper(xs, index + 1, left, k - count)
    
def partition(xs: List[Tuple[int, float]], left: int, right: int):
    p = xs[left]
    i = left + 1
    j = right
    while True:
        while i < right and compare_tuples(xs[i], p) < 0:
            i += 1
        
        while j >= left and compare_tuples(xs[j], p) > 0:
            j -= 1
        
        if i >= j:
            break
        
        temp = xs[j]
        xs[j] = xs[i]
        xs[i] = temp
    # print(j) 
    temp = xs[left]
    xs[left] = xs[i]
    xs[i] = temp
    return i


    