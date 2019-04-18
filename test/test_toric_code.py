from toric_matching.toric_code import manhattan_distance, Toric_Code


def test_manhattan_distance():
    vertex_pairs = [((0, 0), (2, 2)), ((1, 1, 1), (0, 2, 4)),
                    ((0, 1, 2, 3), (3, 3, 3, 3))]
    ls = [3, 5, 4]
    distances = [2, 4, 4]
    for i in range(len(vertex_pairs)):
        assert(manhattan_distance(
            vertex_pairs[i][0], vertex_pairs[i][1], ls[i]) == distances[i])
