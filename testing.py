from data_structures.bst import BinarySearchTree, BSTInOrderIterator

bst = BinarySearchTree()
bst[5] = "M"
bst[3] = "L"
bst[7] = "R"
bst[2] = "LL"
bst[4] = "LR"
bst[6] = "RL"
bst[8] = "RR"

in_nodes   = [node.key for node in BSTInOrderIterator(bst.root)]
print(in_nodes)