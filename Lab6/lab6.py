from queue import Queue


class Node:
    def __init__(self, parent=None, letter=None, fail_node=None, state_num=0):
        self.parent = parent
        self.letter = letter  # letter by which the parent connects to the child
        self.children = dict()
        self.fail_node = fail_node
        self.state_num = state_num  # state_num > 0 indicate accepting state


class AhoCorasickAutomata:
    def __init__(self, patterns_list):
        self.root = Node()
        for curr_suffix in patterns_list:
            head, index = self.find(curr_suffix)
            self.graft(head, curr_suffix[index:])

        # To this point trie is built, we need to make fail_nodes now
        self.add_state_nums(patterns_list)
        self.add_fail_nodes()

    def find(self, text):
        curr_node = self.root
        i = 0
        while i < len(text) and text[i] in curr_node.children:
            curr_node = curr_node.children[text[i]]
            i += 1
        return curr_node, i

    def graft(self, node, text):
        for ch in text:
            new_node = Node(node, ch, self.root)  # creating new node with node as a parent
            node.children[ch] = new_node  # adding new node to children of current node
            node = new_node

    def search(self, substring):  # we don't count the $ sign at the end
        found_node, index = self.find(substring)
        return found_node.children == {} and index == len(substring)

    def add_fail_nodes(self):
        queue = Queue()
        queue.put(self.root)

        while not queue.empty():
            node = queue.get()
            if node != self.root and node.parent != self.root:
                parent_node, letter = node.parent, node.letter
                curr_fail = parent_node.fail_node
                while curr_fail != parent_node and letter not in parent_node.children:
                    curr_fail = curr_fail.fail_node
                if letter in curr_fail.children:
                    node.fail_node = curr_fail.children[letter]

            for letter, child_node in node.children.items():
                queue.put(child_node)

    def add_state_nums(self, list_of_patterns):
        acc, already_seen = 0, set()
        for pattern in list_of_patterns:
            if pattern not in already_seen:
                node = self.root
                for character in pattern:
                    node = node.children[character]
                acc += 1
                node.state_num = acc
                already_seen.add(pattern)

    def traverse_line(self, elem_list):  # elem_list: int list, returns int list
        state = self.root
        result = []
        for elem in elem_list:
            while state is not None and elem not in state.children:
                state = state.fail_node
            if state is None:
                state = self.root
            else:
                state = state.children[elem]
            result.append(state.state_num)
        return result

    def print_aho_corasick(self, node=None):
        if node is None:  node = self.root
        print(f"Curr node={node.state_num}")
        print(f"Fail_node={node.fail_node.state_num}")
        for child in node.children.values():
            self.print_aho_corasick(child)


def compute_pi(pattern):
    m = len(pattern)
    pi = [0 for _ in range(m)]
    k = 0
    for q in range(1, m):
        while k > 0 and pattern[k] != pattern[q]:
            k = pi[k - 1]
        if pattern[k] == pattern[q]:
            k += 1
        pi[q] = k
    return pi


def pattern_matching_KMP(word, pattern, pi=None):
    result = []
    n, m, q = len(word), len(pattern), 0
    if pi is None: pi = compute_pi(pattern)

    for i in range(n):
        while q > 0 and pattern[q] != word[i]:
            q = pi[q - 1]
        if pattern[q] == word[i]:
            q += 1
        if q == m:
            result.append(i - q + 1)
            q = pi[q - 1]
    return result


def find_2d_pattern(elem_2d_list, patterns_list):
    def pattern_to_int_list():
        acc, already_seen = 0, dict()
        result = []
        for pattern in patterns_list:
            if pattern not in already_seen:
                acc += 1
                already_seen[pattern] = acc
            result.append(already_seen[pattern])
        return result

    def divide_column_into_words(no_col, low_threshold, n):
        result = {}
        i = 0
        while i < n:
            start = i
            new_word = []
            while i < n and no_col < len(matched_patterns_array[i]):
                new_word.append(matched_patterns_array[i][no_col])
                i += 1
            if len(new_word) >= low_threshold:
                result[start] = new_word
            i += 1
        return result

    n, m = len(elem_2d_list), len(patterns_list)
    aho_corasick = AhoCorasickAutomata(patterns_list)
    matched_patterns_array = [aho_corasick.traverse_line(line) for line in elem_2d_list]
    pattern_to_find = pattern_to_int_list()
    max_line_len = max([len(line) for line in elem_2d_list])

    result = []
    for i in range(max_line_len):
        words_in_column = divide_column_into_words(i, m, n)
        for row_num, word in words_in_column.items():
            matched_2d_patterns = pattern_matching_KMP(word, pattern_to_find)
            for relative_row_num in matched_2d_patterns:
                pattern_position = (row_num + relative_row_num, i)
                result.append(pattern_position)
    return result

test_table = ["this is a test",
              "this is really fine",
              "this is fine",
              "this is fun",
              "this is a test",
              "this is fine",
              "this is really fun"
              ]
print(find_2d_pattern(test_table, ["this", "this", "this"]))
