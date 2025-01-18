from typing import List, Tuple
from sklearn.decomposition import PCA
import numpy as np 
from app.algorithm.Pair import Pair


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

def quick_select(pairs: List[Tuple[int, float]]):
    pass