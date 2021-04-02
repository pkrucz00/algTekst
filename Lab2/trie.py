texts = ["bbbd", "aabbabd", "ababcd", "abcbccd"]
text_from_the_file = '''
    Dz.U. z 1998 r. Nr 144, poz. 930




                                    USTAWA
                          z dnia 20 listopada 1998 r.

         o zryczałtowanym podatku dochodowym od niektórych przychodów
                        osiąganych przez osoby fizyczne

                                  Rozdział 1
                                Przepisy ogólne

                                    Art. 1.
Ustawa reguluje opodatkowanie zryczałtowanym podatkiem dochodowym niektórych
przychodów (dochodów) osiąganych przez osoby fizyczne prowadzące pozarolniczą
działalność gospodarczą oraz przez osoby duchowne.

                                    Art. 2.
1. Osoby fizyczne osiągające przychody z pozarolniczej działalności
  gospodarczej opłacają zryczałtowany podatek dochodowy w formie:
   1) ryczałtu od przychodów ewidencjonowanych,
   2) karty podatkowej.
2. Osoby duchowne, prawnie uznanych wyznań, opłacają zryczałtowany podatek
  dochodowy od przychodów osób duchownych.
3. Wpływy z podatku dochodowego opłacanego w formie ryczałtu od przychodów
  ewidencjonowanych oraz zryczałtowanego podatku dochodowego od przychodów
  osób duchownych stanowią dochód budżetu państwa.
4. Wpływy z karty podatkowej stanowią dochody gmin.

                                    Art. 3.
Przychodów (dochodów) opodatkowanych w formach zryczałtowanych nie łączy się z
przychodami (dochodami) z innych źródeł podlegającymi opodatkowaniu na
podstawie ustawy z dnia 26 lipca 1991 r. o podatku dochodowym od osób
fizycznych (Dz. U. z 1993 r. Nr 90, poz. 416 i Nr 134, poz. 646, z 1994 r. Nr
43, poz. 163, Nr 90, poz. 419, Nr 113, poz. 547, Nr 123, poz. 602 i Nr 126,
poz. 626, z 1995 r. Nr 5, poz. 25 i Nr 133, poz. 654, z 1996 r. Nr 25, poz.
113, Nr 87, poz. 395, Nr 137, poz. 638, Nr 147, poz. 686 i Nr 156, poz. 776, z
1997 r. Nr 28, poz. 153, Nr 30, poz. 164, Nr 71, poz. 449, Nr 85, poz. 538, Nr
96, poz. 592, Nr 121, poz. 770, Nr 123, poz. 776, Nr 137, poz. 926, Nr 139,
poz. 932-934 i Nr 141, poz. 943 i 945 oraz z 1998 r. Nr 66, poz. 430, Nr 74,
poz. 471, Nr 108, poz. 685 i Nr 117, poz. 756), zwanej dalej "ustawą o podatku
dochodowym".
'''
texts.append(text_from_the_file)

texts = list(map(lambda x: x + "$", texts))


class Node:
    def __init__(self, parent):
        self.parent = parent
        self.children = dict()


class Trie:
    def __init__(self, text):
        self.root = Node(None)
        self.break_sign = '$'
        for i in range(len(text)):
            curr_suffix = text[i:]
            head, index = self.find(curr_suffix)
            self.graft(head, curr_suffix[index:])

    def find(self, text):
        curr_node = self.root
        i = 0
        while i < len(text) and text[i] in curr_node.children:
            curr_node = curr_node.children[text[i]]
            i += 1
        return curr_node, i

    def graft(self, node, text):
        for ch in text:
            new_node = Node(node)  # creating new node with node as a parent
            node.children[ch] = new_node  # adding new node to children of current node
            node = new_node

    def search_substring(self, substring):
        found_node, index = self.find(substring)
        return found_node.children != {} and index == len(substring)

    def print_trie(self, node=None):
        if node is None:  node = self.root
        print(node.children)
        for child in node.children.values():
            self.print_trie(child)


class SuffixTreeNode:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.children = dict()
        # elf.start_index = start_index


class SuffixTree:
    def __init__(self, text):
        self.root = SuffixTreeNode(0, len(text) - 1)
        self.full_text = text
        for i in range(len(text) - 1):
            curr_suff = text[i:]
            head, depth = self.slow_find(curr_suff)
            self.graft(head, depth, i)

    def graft(self, head, depth, i):
        new_node = SuffixTreeNode(depth + i, len(self.full_text) - 1)
        head.children[self.full_text[new_node.start]] = new_node

    def slow_find(self, text, depth=0, curr_node=None):  # return head; depth - length of the longest prefix of text
        # in suffix tree
        if curr_node is None: curr_node = self.root

        first_letter = text[0]
        next_node = curr_node.children.get(first_letter)

        if next_node is None:
            return curr_node, depth
        start, end = next_node.start, next_node.end
        childs_text_len = end - start + 1
        for i in range(1, childs_text_len):
            if self.full_text[start + i] != text[i]:
                return self.break_path(i, curr_node, next_node), depth + i
        return self.slow_find(text[childs_text_len:], depth + childs_text_len, next_node)

    def break_path(self, index, parent_node, next_node):
        old_start, old_end = next_node.start, next_node.end
        break_node = SuffixTreeNode(old_start, old_start + index - 1)
        next_node.start = old_start + index

        parent_node.children[self.full_text[break_node.start]] = break_node #wskazanie po literce na nowy node
        break_node.children[self.full_text[next_node.start]] = next_node  # wskazanie po literce na dotychczasowy node
        return break_node

    def search(self, substring, curr_node=None):
        if len(substring) == 0:
            return True

        if curr_node is None:
            curr_node = self.root

        first_letter = substring[0]
        next_node = curr_node.children.get(first_letter)
        if next_node is None:
            return False

        childs_text_len = next_node.end - next_node.start + 1
        for i in range(1, childs_text_len):
            if i == len(substring):
                return True
            if self.full_text[next_node.start + i] != substring[i]:
                return False

        return self.search(substring[childs_text_len:], next_node)



for text in texts:
    iHopeItWillWork = SuffixTree(text)
    for i in range(0, len(text)):
        for j in range(i, len(text)):
            if not iHopeItWillWork.search(text[i:j]):
                print(text[i:j])


