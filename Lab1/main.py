def compute_delta(pattern, alphabet):
    def is_suffix(potential_suffix, main_word):
        m = len(potential_suffix)
        return main_word[-m:] == potential_suffix

    m = len(pattern)
    delta = [dict() for _ in range(m+1)]
    for q in range(m + 1):
        for elem in alphabet:
            k = min(m, q + 1)
            while k > 0 and not is_suffix(pattern[:k], pattern[:q] + elem):
                k -= 1
                print(k)
            delta[q][elem] = k
    return delta

print(compute_delta("ababaca", "abc"))
日一大年中会人本月長国出上十生子分東三行同今高金時手見市力米自前円合立内二事社者地京間田体学下目五後新明方部.女八心四民対主正代言九小思七山実入回場野開万全定家北六問話文動度県水安氏和政保表道相意発不党