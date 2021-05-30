from math import sqrt, inf
from sklearn.cluster import DBSCAN


FILE_PATH = "lines.txt"


def lcs(text_a, text_b):
    m, n = len(text_a), len(text_b)
    similarities = [[0 for _ in range(n + 1)] for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text_a[i - 1] == text_b[j - 1]:
                similarities[i][j] = similarities[i - 1][j - 1] + 1
            else:
                similarities[i][j] = similarities[i - 1][j - 1]

    return 1 - max([max(row) for row in similarities]) / max(m, n)


def dice(text_a, text_b, k):
    def make_n_grams_set(text):
        return {text[i:i + k] for i in range(len(text) - k + 1)}

    set_a = make_n_grams_set(text_a)
    set_b = make_n_grams_set(text_b)
    common_grams = len(set_a.intersection(set_b))
    len_a, len_b = len(set_a), len(set_b)

    return 1 - 2 * common_grams / (len_a + len_b)


def cosine(text_a, text_b, k):
    def make_n_gram_dict(text):
        result_dict = dict()
        for i in range(len(text) - k + 1):
            n_gram = text[i: i + k]
            result_dict.setdefault(n_gram, 0)
            result_dict[n_gram] += 1
        return result_dict

    def vec_sum(dict_vec):
        return sqrt(sum(map(lambda x: x**2, dict_vec.values())))

    dict_a, dict_b = make_n_gram_dict(text_a), make_n_gram_dict(text_b)
    len_a, len_b = vec_sum(dict_a), vec_sum(dict_b)

    scalar_value = 0
    for key_a, val_a in dict_a.items():
        if key_a in dict_b:
            val_b = dict_b[key_a]
            scalar_value += val_a * val_b

    return 1 - scalar_value/(len_a*len_b)

def k_cosine(k):
    def my_cosine(text_a, text_b):
        return cosine(text_a, text_b, k)
    return my_cosine


def levenshteinDistance(text_a, text_b):
    delta = lambda x, y: 0 if x == y else 1

    len_a = len(text_a)
    len_b = len(text_b)

    dist_table = [[0 for _ in range(len_b + 1)] for _ in range(len_a + 1)]

    for i in range(1, len_a + 1):
        dist_table[i][0] = i
    for j in range(1, len_b + 1):
        dist_table[0][j] = j

    for i in range(1, len_a + 1):
        for j in range(1, len_b + 1):
            x, y = text_a[i - 1], text_b[j - 1]  # current letters

            up_cost, left_cost, diag_cost = dist_table[i - 1][j] + 1, dist_table[i][j - 1] + 1, \
                                            dist_table[i - 1][j - 1] + delta(x, y)
            dist_table[i][j] = min(up_cost, left_cost, diag_cost)

    return dist_table[len_a][len_b]/max(len_a, len_b)

## CLUSTER INDEXES
def dist_between_elems(cluster, dist):
    return [[dist(elem_a, elem_b) for elem_a in cluster] for elem_b in cluster]


def sigma(cluster, dist):
    distances = dist_between_elems(cluster, dist)
    return sum([sum(distances[i]) for i in range(len(distances))])/len(cluster)**2


def centroid(cluster):
    return cluster[0]


def dist_between_clusters(clust_a, clust_b, dist):
    centr_a = centroid(clust_a)
    centr_b = centroid(clust_b)
    return dist(centr_a, centr_b)


def size_of_cluster(cluster, dist):
    distances = dist_between_elems(cluster, dist)
    return max([max(distances[i]) for i in range(len(distances))])


## DAVIES BOULDIN
def davies_bouldin(clusters, dist):
    n = len(clusters)
    sigmas = [sigma(cluster, dist) for cluster in clusters]
    rs = [[(sigmas[i] + sigmas[j])/dist_between_clusters(clusters[i], clusters[j], dist)
           if i != j else 0
          for i in range(n)]
          for j in range(n)]
    d = max(rs)
    return sum(d)/n

#DUNE INDEX

def dunn(clusters, dist):
    distances_between_clusters = [[dist_between_clusters(clusters[i], clusters[j], dist)
                                   if i != j else inf
                                   for j in range(i, len(clusters))]
                                  for i in range(len(clusters))]
    min_dist = min([min(one_clust_dist) for one_clust_dist in distances_between_clusters])
    clust_sizes = [size_of_cluster(cluster, dist) for cluster in clusters]
    max_size = max(clust_sizes)
    return min_dist/max_size

##CLUSTERING



def open_file(path):
    with open(path, "r") as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
    return lines




def matrix_of_similarities(dist, text):
    return [[dist(line_x, line_y) for line_x in text] for line_y in text]


def cluster(text, measure, eps=1, min_sample=1):
    sim_matrix = matrix_of_similarities(measure, text)
    clusters = DBSCAN(eps=eps, min_samples=min_sample).fit_predict(sim_matrix)
    temp_dict = {cluster: [] for cluster in clusters}
    for i in range(len(text)):
        temp_dict[clusters[i]].append(text[i])

    return list(temp_dict.values())

## PODZIAL NA WEKTORY - nieuzywane
# def k_grams_indexed(text, k):
#     indexed_grams = dict()
#     curr_ind = 0
#     for line in text:
#         for i in range(len(line) - k + 1):
#             k_gram = line[i:i+k]
#             if k_gram not in indexed_grams:
#                 indexed_grams[k_gram] = curr_ind
#                 curr_ind += 1
#     return indexed_grams

# def vectorize_text(text, k):
#     def one_hot_line_vector(line):
#         one_hot_vector = [0] * len(k_gram_index)
#         for i in range(len(line) - k + 1):
#             k_gram = line[i:i+k]
#             one_hot_vector[k_gram_index[k_gram]] = 1
#         return one_hot_vector

#     k_gram_index = k_grams_indexed(text, k)
#     result = [one_hot_line_vector(line) for line in lines]
#     return result


if __name__=="__main__":
    text = open_file(FILE_PATH)
    text = text[:20]
    cosine_5_gram = k_cosine(5)
    clusters = cluster(text, cosine_5_gram, eps=1, min_sample=1)
    for clstr in clusters:
        print(clstr)
    print(dunn(clusters, cosine_5_gram))
