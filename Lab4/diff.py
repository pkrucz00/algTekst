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


def diff(seq_a, seq_b):
    _, traceback = lcsequence(seq_a, seq_b)
    line_a, line_b = len(seq_a), len(seq_b)

    differences = []
    while line_a > 0 and line_b > 0:
        if traceback[line_a][line_b] == "diag":
            line_a, line_b = line_a - 1, line_b - 1
        elif traceback[line_a][line_b] == "up":
            differences.append(f'< [{line_a}] {seq_a[line_a-1]} ')
            line_a -= 1
        else:
            differences.append(f'> [{line_b}] {seq_b[line_b-1]}')
            line_b -= 1

    while line_a > 0:
        differences.append(f'< [{line_a}] {seq_a[line_a]}')
        line_a -= 1
    while line_b > 0:
        differences.append(f'> [{line_b}] {seq_b[line_b]}')
        line_b -= 1

    differences.reverse()
    return differences


def get_lines(path):
    with open(path, "r", encoding="UTF-8") as file:
        return [line.strip() for line in file.readlines()]


lines_text_1 = get_lines("romeo_trimmed_1.txt")
lines_text_2 = get_lines("romeo_trimmed_2.txt")

result = diff(lines_text_1, lines_text_2)
for line in result:
    print(line)

