def lcsequence(seq_a, seq_b):
    len_a = len(seq_a)
    len_b = len(seq_b)

    lcs = [[0 for _ in range(len_b + 1)] for _ in range(len_a + 1)]
    traceback = [[None for _ in range(len_b + 1)] for _ in range(len_a + 1)]

    for i in range(1, len_a + 1):
        lcs[i][0] = 0
        traceback[i][0] = "up"
    for j in range(1, len_b + 1):
        lcs[0][j] = 0
        traceback[0][j] = "left"

    for i in range(1, len_a + 1):
        for j in range(1, len_b + 1):
            x, y = seq_a[i - 1], seq_b[j - 1]  # current elements in sequences

            if x == y:
                lcs[i][j] = lcs[i - 1][j - 1] + 1
                traceback[i][j] = "diag"
            elif lcs[i - 1][j] >= lcs[i][j - 1]:
                lcs[i][j] = lcs[i - 1][j]
                traceback[i][j] = "up"
            else:
                lcs[i][j] = lcs[i][j - 1]
                traceback[i][j] = "left"

    return lcs[len_a][len_b], traceback


longest, traceback = lcsequence(["A", "B", "C", "B", "D", "A", "B"], ["B", "D", "C", "A", "B", "A"])
print(longest)