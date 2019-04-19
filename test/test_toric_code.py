from toric_matching.toric_code import manhattan_distance, ToricCode


def test_manhattan_distance():
    vertex_pairs = [((0, 0), (2, 2)), ((1, 1, 1), (0, 2, 4)),
                    ((0, 1, 2, 3), (3, 3, 3, 3))]
    ls = [3, 5, 4]
    distances = [2, 4, 4]
    for i in range(len(vertex_pairs)):
        assert(manhattan_distance(
            vertex_pairs[i][0], vertex_pairs[i][1], ls[i]) == distances[i])

def test_calculate_syndrome():
    for l in [3, 5]:
        # 2D test
        code = ToricCode(2, l)
        # Single qubit error
        code.lattice[(0, 0)][(0, 1)]['qubit_state'] = 1
        code.calculate_syndrome()
        for node in code.lattice.nodes():
            if node == (0, 0) or node == (0, 1):
                assert(code.lattice.node[node]['stabilizer_value'] == 1)
            else:
                assert(code.lattice.node[node]['stabilizer_value'] == 0)
        # Two qubit error
        code.lattice[(0, 1)][(1, 1)]['qubit_state'] = 1
        code.calculate_syndrome()
        for node in code.lattice.nodes():
            if node == (0, 0) or node == (1, 1):
                assert(code.lattice.node[node]['stabilizer_value'] == 1)
            else:
                assert(code.lattice.node[node]['stabilizer_value'] == 0)
        # Stabilizer error
        code.lattice[(0, 0)][(1, 0)]['qubit_state'] = 1
        code.lattice[(1, 0)][(1, 1)]['qubit_state'] = 1
        code.calculate_syndrome()
        for node in code.lattice.nodes():
            assert(code.lattice.node[node]['stabilizer_value'] == 0)

        # 3D test
        code = ToricCode(3, l)
        # Single qubit error
        code.lattice[(1, 1, 1)][(1, 1, 2)]['qubit_state'] = 1
        code.calculate_syndrome()
        for node in code.lattice.nodes():
            if node == (1, 1, 1) or node == (1, 1, 2):
                assert(code.lattice.node[node]['stabilizer_value'] == 1)
            else:
                assert(code.lattice.node[node]['stabilizer_value'] == 0)
        # Two qubit error
        code.lattice[(1, 1, 2)][(1, 2, 2)]['qubit_state'] = 1
        code.calculate_syndrome()
        for node in code.lattice.nodes():
            if node == (1, 1, 1) or node == (1, 2, 2):
                assert(code.lattice.node[node]['stabilizer_value'] == 1)
            else:
                assert(code.lattice.node[node]['stabilizer_value'] == 0)
        # Stabilizer error
        code.lattice[(1, 1, 1)][(1, 2, 1)]['qubit_state'] = 1
        code.lattice[(1, 2, 1)][(1, 2, 2)]['qubit_state'] = 1
        code.calculate_syndrome()
        for node in code.lattice.nodes():
            assert(code.lattice.node[node]['stabilizer_value'] == 0)

        # 4D test
        code = ToricCode(4, l)
        # Single qubit error
        code.lattice[(0, 0, 0, 2)][(0, 0, 1, 2)]['qubit_state'] = 1
        code.calculate_syndrome()
        for node in code.lattice.nodes():
            if node == (0, 0, 0, 2) or node == (0, 0, 1, 2):
                assert(code.lattice.node[node]['stabilizer_value'] == 1)
            else:
                assert(code.lattice.node[node]['stabilizer_value'] == 0)
        # Two qubit error
        code.lattice[(0, 0, 1, 2)][(0, 1, 1, 2)]['qubit_state'] = 1
        code.calculate_syndrome()
        for node in code.lattice.nodes():
            if node == (0, 0, 0, 2) or node == (0, 1, 1, 2):
                assert(code.lattice.node[node]['stabilizer_value'] == 1)
            else:
                assert(code.lattice.node[node]['stabilizer_value'] == 0)
        # Stabilizer error
        code.lattice[(0, 1, 0, 2)][(0, 1, 1, 2)]['qubit_state'] = 1 
        code.lattice[(0, 0, 0, 2)][(0, 1, 0, 2)]['qubit_state'] = 1
        code.calculate_syndrome()
        for node in code.lattice.nodes():
            assert(code.lattice.node[node]['stabilizer_value'] == 0)

