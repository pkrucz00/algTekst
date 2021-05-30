from bitarray import bitarray
from queue import Queue

from bitarray.util import ba2int


class InternalNode:
    def __init__(self, left, right, weight, parent=None, index=None):
        self.weight = weight
        self.left = left
        self.right = right
        self.parent = parent
        self.index = index


class Leaf:
    def __init__(self, letter, weight, parent=None, index=None):
        self.weight = weight
        self.letter = letter
        self.parent = parent
        self.index = index


N_BYTES = 2
K_BYTES = 3


def is_instance(obj, class_name):
    return obj.__class__.__name__ == class_name


def get_node_code(curr_node):  # we go up the tree till we get parent
    result = bitarray()
    while curr_node is not None:
        dad = curr_node.parent
        if dad is not None and dad.left is curr_node:
            result.append(False)
        elif dad is not None and dad.right is curr_node:
            result.append(True)
        curr_node = dad

    return result[::-1]  # reversing since we go up the tree (normally we go down)


def update_indexes(root):
    queue = Queue()
    queue.put(root)
    i = 0

    while not queue.empty():
        curr_node = queue.get()
        curr_node.index = i
        if is_instance(curr_node, "InternalNode"):
            queue.put(curr_node.right)
            queue.put(curr_node.left)
        i += 1


# def get_leader(curr_node, nodes):
#     if is_instance(curr_node, "Leaf") and curr_node.letter == 'o':
#         print("Hello")
#     nodes_with_the_same_weight = nodes[curr_node.weight]
#     leader = min(nodes_with_the_same_weight, key=lambda x: x.index)
#     return leader


def increment(curr_node, nodes):  # go up the huffman tree, increment every node and swap if necessary
    def swap_condition(curr, weight_leader):
        return curr.parent is not None and weight_leader. parent is not None and \
               curr is not weight_leader.parent and curr.parent is not weight_leader and\
               weight_leader.index < curr.index

    def swap(node_a, node_b):
        if node_a.parent is node_b.parent:
            if node_a.parent.left is node_a:
                node_a.parent.left = node_b
                node_a.parent.right = node_a
            else:
                node_a.parent.left = node_a
                node_a.parent.right = node_b
            return
        node_a_parent = node_a.parent
        node_b_parent = node_b.parent
        if node_a is node_a_parent.left:
            node_a_parent.left = node_b
        else:
            node_a_parent.right = node_b
        if node_b is node_b_parent.left:
            node_b_parent.left = node_a
        else:
            node_b_parent.right = node_a
        node_a.parent = node_b_parent
        node_b.parent = node_a_parent
        node_a.index, node_b.index = node_b.index, node_a.index

    while curr_node.parent is not None:
        # if is_instance(curr_node, "Leaf") and curr_node.letter == 'k':
        #     print("Hello")

        leaders = nodes[curr_node.weight]
        leaders.sort(key=lambda x: x.index)
        i = 0
        while i < len(leaders) and leaders[i].index < curr_node.index:
            leader = leaders[i]
            if swap_condition(curr_node, leader):
                swap(curr_node, leader)
                break
            i += 1

        add_weight_and_update_nodes(nodes, curr_node)
        curr_node = curr_node.parent

    add_weight_and_update_nodes(nodes, curr_node)
    update_indexes(curr_node)


def add_weight_and_update_nodes(nodes, curr_node):
    old_weight_buddies = nodes[curr_node.weight]
    if curr_node in old_weight_buddies:
        old_weight_buddies.remove(curr_node)

    curr_node.weight += 1

    list_with_nodes_with_the_same_weigth = nodes.setdefault(curr_node.weight, [])
    list_with_nodes_with_the_same_weigth.append(curr_node)


def copy_leaf(leaf_node):  # make new InternalNode out of a given Leaf
    new_node = InternalNode(None, None, leaf_node.weight, parent=leaf_node.parent)
    if leaf_node.parent is not None:
        if leaf_node.parent.left is leaf_node:
            new_node.parent.left = new_node
        else:
            new_node.parent.right = new_node

    return new_node


def add_new_letter(zero_node, letter, leaves, nodes, root):  # making and rearranging the tree
    new_internal = copy_leaf(zero_node)  # making internal node out of the zero node and attaching it to parent

    new_leaf = Leaf(letter, 0, parent=new_internal)
    add_weight_and_update_nodes(nodes, new_leaf)
    new_internal.right = new_leaf
    leaves[letter] = new_leaf

    new_internal.left = zero_node
    zero_node.parent = new_internal

    if new_internal.parent is None:
        root = new_internal

    update_indexes(root)
    increment(new_internal, nodes)
    return new_internal


# nyt means "not yet transmitted" - it's the "zero" node
def adaptive_huffman_encode(text):
    nyt_char = '\uE000'  # special character in UNICODE
    leaves = {nyt_char: Leaf(nyt_char, 0, parent=None, index=0)}
    encoded_text = bitarray()
    root = leaves[nyt_char]

    nodes = {0: [root]}

    for letter in text:
        if letter in leaves:
            curr_node = leaves[letter]
            node_code = get_node_code(curr_node)
            encoded_text += node_code

            increment(curr_node, nodes)
        else:
            zero_node = leaves[nyt_char]

            zero_node_code = get_node_code(zero_node)
            encoded_text += zero_node_code
            letter_bytes = ord(letter).to_bytes(length=N_BYTES, byteorder='big', signed=False)
            encoded_text.frombytes(letter_bytes)

            new_internal = add_new_letter(zero_node, letter, leaves, nodes, root)
            if new_internal.parent is None:  # new_internal is the factual root
                root = new_internal  # so we need to change it

    return root, encoded_text


def adaptive_huffman_decode(code):
    nyt_char = '\uE000'  # special character in UNICODE
    leaves = {nyt_char: Leaf(nyt_char, 0, parent=None)}
    decoded_text = ""
    root = leaves[nyt_char]

    nodes = {0: [root]}
    acc = 0
    i = 0
    while i < len(code):
        curr_node = root
        while is_instance(curr_node, "InternalNode"):
            bit = code[i]
            if bit == 0:
                curr_node = curr_node.left
            else:
                curr_node = curr_node.right
            i += 1

        if curr_node.letter != nyt_char:  # the letter was previously in text
            letter = curr_node.letter
            decoded_text += letter
            increment(curr_node, nodes)
        else:                             # the first encounter of the letter (curr_node is zero_node)
            letter = chr(ba2int(code[i:i + 8 * N_BYTES], signed=False))
            i += 8 * N_BYTES
            decoded_text += letter
            acc += 1

            zero_node = leaves[nyt_char]

            new_internal = add_new_letter(zero_node, letter, leaves, nodes, root)
            if new_internal.parent is None:  # new_internal is the factual root
                root = new_internal  # so we need to change it

    print(f'Number of added characters: {acc}')
    return decoded_text


root, encoded = adaptive_huffman_encode("abracadabra")
print(encoded)
decoded = adaptive_huffman_decode(encoded)
print(decoded)
