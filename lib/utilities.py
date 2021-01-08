def combine_unique(list_1, list_2):
    for element in list_2:
        if element in list_1: continue
        else: list_1.append(element)
    return list_1
    
def add_coordinates(coord_1, coord_2):
    x1, y1 = coord_1
    x2, y2 = coord_2
    return (x1+x2, y1+y2)