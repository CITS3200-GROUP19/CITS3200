# Function that maps data to comment
# PROTOTYPE
# Only works nicely on right eye currently
def right_comment_map(data_pairs):
    # Top Row
    print('         -', end=' ')
    for x in range(6, 10):
        if x in data_pairs:
            print(data_pairs[x], end=' ')
    print('-')
    # 2nd Row
    print('      -', end=' ')
    for x in range(12, 18):
        if x in data_pairs:
            print(data_pairs[x], end=' ')
    print('-')
    # 3rd Row
    print('   -', end=' ')
    for x in range(20, 28):
        if x in data_pairs:
            print(data_pairs[x], end=' ')
    print('-')
    # 4th Row
    print('-', end=' ')
    for x in range(29, 39):
        if x in data_pairs:
            print(data_pairs[x], end=' ')
    print('-')
    # 5th Row
    print('-', end=' ')
    for x in range(39, 49):
        if x in data_pairs:
            print(data_pairs[x], end=' ')
    print('-')
    # 6th Row
    print('   -', end=' ')
    for x in range(50, 58):
        if x in data_pairs:
            print(data_pairs[x], end=' ')
    print('-')
    # 7th Row
    print('      -', end=' ')
    for x in range(60, 66):
        if x in data_pairs:
            print(data_pairs[x], end=' ')
    print('-')
    # 8th Row
    print('         -', end=' ')
    for x in range(68, 72):
        if x in data_pairs:
            print(data_pairs[x], end=' ')
    print('-')
# Print commented map of vf data
