def combine_unique(list_1, list_2):
    for element in list_2:
        if element in list_1: continue
        else: list_1.append(element)
    return list_1