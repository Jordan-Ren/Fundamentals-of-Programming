"""6.009 Lab 4 -- Tent Packing"""

# NO IMPORTS ALLOWED!


# Example bag_list entries:
#      vertical 3x1 bag: { (0,0), (1,0), (2,0) }
#      horizontal 1x3 bag: { (0,0), (0,1), (0,2) }
#      square bag: { (0,0), (0,1), (1,0), (1,1) }
#      L-shaped bag: { (0,0), (1,0), (1,1) }
#      C-shaped bag: { (0,0), (0,1), (1,0), (2,0), (2,1) }
#      reverse-C-shaped bag: { (0,0), (0,1), (1,1), (2,0), (2,1) }


def pack(tent_size, missing_squares, bag_list, max_vacancy):
    """
    Pack a tent with different sleeping bag shapes leaving up to max_vacancy squares open
    :param tent_size: (rows, cols) for tent grid
    :param missing_squares: set of (r, c) tuples giving location of rocks
    :param bag_list: list of sets, each describing a sleeping bag shape
    Each set contains (r, c) tuples enumerating contiguous grid
    squares occupied by the bag, coords are relative to the upper-
    left corner of the bag.  You can assume every bag occupies
    at least the grid (0,0).
    :param max_vacancy: maximum number of non-rock locations which can be unoccupied
    :return:  None if no packing can be found; otherwise a list giving the
    placement and type for each placed bag expressed as a dictionary
    with keys
        "anchor": (r, c) for upper-left corner of bag
        "shape": index of bag on bag list
    """
    occupied = set()
    final = []
    for i in missing_squares:
        occupied.add(i)
    def helper(tent_size, bag_list, max_vacancy,  final = [], occupied = set(), vacant = None):
        possible = get_possible(tent_size, occupied, vacant)
        if len(vacant) > max_vacancy:
            return False
        if len(occupied) >= (tent_size[0] * tent_size[1] -  max_vacancy):
            return True
        for coord in possible:
            for i in range(6):
                new_bag = create_bag_coords(coord, bag_list[i])
                if is_safe(tent_size, new_bag, occupied):
                    dict = {"anchor": coord, "shape": i}
                    final.append(dict)
                    for x in new_bag:
                        occupied.add(x)
                    if helper(tent_size, bag_list, max_vacancy, final, occupied, vacant):
                        return final
                    for x in new_bag:
                        occupied.remove(x)
                    final.remove(dict)
            vacant.append(coord)
            if helper(tent_size, bag_list, max_vacancy, final, occupied, vacant):
                return final
            else:
                del vacant[-1]
                return None
        return None
    result = helper(tent_size, bag_list, max_vacancy, final, occupied, [])
    return result

def get_possible(tent_size, occupied, vacant):
    coords = []
    for row in range(tent_size[0]):
        for col in range(tent_size[1]):
            if (row, col) not in occupied and (row,col) not in vacant:
                coords.append((row,col))
    return coords

def is_safe(tent_size, new_bag, occupied):
    for i in new_bag:
        if i[0] <= tent_size[0] - 1 and i[1] <= tent_size[1] - 1:
            if i[0] >= 0 and i[1] >= 0:
                if i in occupied:
                    return False
            else:
                return False
        else:
            return False
    return True

def create_bag_coords(coord, bag_list):
    new_bag = set()
    for j in bag_list:
        new_bag.add((j[0] + coord[0], j[1] + coord[1]))
    return  new_bag




bag_list = [
    {(0, 0), (1, 0), (2, 0)},  # vertical 3x1 bag
    {(0, 0), (0, 1), (0, 2)},  # horizontal 1x3 bag
    {(0, 0), (0, 1), (1, 0), (1, 1)},  # square bag
    {(0, 0), (1, 0), (1, 1)},  # L-shaped bag
    {(0, 0), (0, 1), (1, 0), (2, 0), (2, 1)},  # C-shaped bag
    {(0, 0), (0, 1), (1, 1), (2, 0), (2, 1)},  # reverse C-shaped bag
]


if __name__ == '__main__':
    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    print(pack((4,4), set(), bag_list, 0))
    # print(is_safe((2,2), bag_list[2], {(0,1)}, (0,0)))
    pass
