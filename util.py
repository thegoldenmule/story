def traverse(tree, leaf_func):
    if tree is None:
        return

    try:
        tree.label()
    except AttributeError:
        leaf_func(tree)
    else:
        for child in tree:
            traverse(child, leaf_func)