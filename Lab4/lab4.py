def levenshteinDistance(text_a, text_b):
    delta = lambda x, y: 0 if x == y else 1

    len_a = len(text_a)
    len_b = len(text_b)

    dist_table = [[0 for _ in range(len_b + 1)] for _ in range(len_a + 1)]
    traceback_table = [[None for _ in range(len_b + 1)] for _ in range(len_a + 1)]

    for i in range(1, len_a + 1):
        dist_table[i][0] = i
        traceback_table[i][0] = "up"
    for j in range(1, len_b + 1):
        dist_table[0][j] = j
        traceback_table[0][j] = "left"

    for i in range(1, len_a + 1):
        for j in range(1, len_b + 1):
            x, y = text_a[i - 1], text_b[j - 1]  # current letters

            up_cost, left_cost, diag_cost = dist_table[i - 1][j] + 1, dist_table[i][j - 1] + 1, \
                                            dist_table[i - 1][j - 1] + delta(x, y)

            if up_cost < left_cost and up_cost < diag_cost:
                dist_table[i][j] = up_cost
                traceback_table[i][j] = "up"
            elif left_cost < diag_cost:
                dist_table[i][j] = left_cost
                traceback_table[i][j] = "left"
            else:
                dist_table[i][j] = diag_cost
                traceback_table[i][j] = "diag"

    return dist_table[len_a][len_b], traceback_table


def editionVisualization(text_a, text_b):
    _, traceback_table = levenshteinDistance(text_a, text_b)
    i = len(text_a)
    j = len(text_b)

    steps = []
    curr_step = traceback_table[i][j]

    while curr_step is not None:
        steps.append(curr_step)

        if curr_step == "up":
            i -= 1
        elif curr_step == "left":
            j -= 1
        elif curr_step == "diag":
            i -= 1
            j -= 1
        else:
            raise AssertionError("Unknown Step")

        curr_step = traceback_table[i][j]

    steps.reverse()

    modified_string = text_a

    for step in steps:
        letter_a, letter_b = modified_string[i], text_b[j]
        if step == "up":
            print(f"{modified_string[:i]}\{letter_a}/{modified_string[i+1:]}")
            modified_string = modified_string[:i] + modified_string[i+1:]
        elif step == "left":
            print(f"{modified_string[:i]}+{letter_b}+{modified_string[i:]}")
            modified_string = modified_string[:i] + letter_b + modified_string[i:]
            j += 1
            i += 1
        elif step == "diag":
            if letter_a != letter_b:
                print(f"{modified_string[:i]}*{letter_b}*{modified_string[i+1:]}")
                modified_string = modified_string[:i] + letter_b + modified_string[i+1:]
            i += 1
            j += 1


editionVisualization("dziewczynki", "witaminki")
