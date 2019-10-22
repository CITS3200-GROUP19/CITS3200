
def data_table_map(data_pairs, data_table):
    # Top Row
    i = 3
    for x in range(6, 10):
        if x in data_pairs:
            data_table[0][i] = data_pairs[x]
        i = i + 1
    i = 2
    # 2nd Row
    for x in range(12, 18):
        if x in data_pairs:
            data_table[1][i] = data_pairs[x]
        i = i + 1
    i = 1
    # 3rd Row
    for x in range(20, 28):
        if x in data_pairs:
            data_table[2][i] = data_pairs[x]
        i = i + 1
    i = 0
    # 4th Row
    for x in range(29, 39):
        if x in data_pairs:
            data_table[3][i] = data_pairs[x]
        i = i + 1
    i = 0
    # 5th Row
    for x in range(39, 49):
        if x in data_pairs:
            data_table[4][i] = data_pairs[x]
        i = i + 1
    i = 1
    # 6th Row
    for x in range(50, 58):
        if x in data_pairs:
            data_table[5][i] = data_pairs[x]
        i = i + 1
    i = 2
    # 7th Row
    for x in range(60, 66):
        if x in data_pairs:
            data_table[6][i] = data_pairs[x]
        i = i + 1
    i = 3
    # 8th Row
    for x in range(68, 72):
        if x in data_pairs:
            data_table[7][i] = data_pairs[x]
        i = i + 1
    i = 0

